import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { detectRepoRoot } from "./repoDetector.js";
import { EventBus } from "./eventBus.js";
import { QueueStore } from "./queueStore.js";
import { WorkerRunner } from "./workerRunner.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const appRoot = path.resolve(here, "..");
const publicRoot = path.join(appRoot, "public");
const dataRoot = path.join(appRoot, "data");
const repo = detectRepoRoot();
const store = new QueueStore(path.join(dataRoot, "mini_arcade_queue.json"));
const bus = new EventBus(() => store.snapshot(repo));
const runner = new WorkerRunner(store, repo, () => bus.emit());

function sendJson(res, status, payload) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(payload));
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  if (!chunks.length) return {};
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

function serveStatic(req, res) {
  const urlPath = new URL(req.url, "http://localhost").pathname;
  const target = path.join(publicRoot, urlPath === "/" ? "index.html" : urlPath);
  if (!target.startsWith(publicRoot) || !fs.existsSync(target) || fs.statSync(target).isDirectory()) {
    res.writeHead(404);
    res.end("not found");
    return;
  }
  const ext = path.extname(target);
  const type = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "text/javascript",
  }[ext] || "application/octet-stream";
  res.writeHead(200, { "Content-Type": type });
  fs.createReadStream(target).pipe(res);
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://localhost");
    if (req.method === "GET" && url.pathname === "/api/status") {
      sendJson(res, 200, store.snapshot(repo));
      return;
    }
    if (req.method === "GET" && url.pathname === "/api/events") {
      bus.connect(res);
      return;
    }
    if (req.method === "GET" && url.pathname === "/favicon.ico") {
      res.writeHead(204);
      res.end();
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/queue") {
      const body = await readBody(req);
      const job = store.addJob(body.flags || {});
      bus.emit();
      sendJson(res, 200, job);
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/queue/batch") {
      const body = await readBody(req);
      const seeds = body.jobs || [];
      const jobs = seeds.map((flags) => store.addJob(flags));
      bus.emit();
      sendJson(res, 200, jobs);
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/launch-auto-build") {
      const body = await readBody(req);
      store.updateSettings({ ...(body.settings || {}), mode: "auto-build" });
      const flags = body.flags || {};
      const job = store.addJobWithMeta({
        flags: {
          idea: String(flags.idea || "").trim(),
          theme: String(flags.theme || "").trim(),
          mechanic: String(flags.mechanic || "").trim(),
          content: String(flags.content || "").trim(),
          depth: String(flags.depth || "quick").trim(),
          mode: String(flags.mode || "").trim(),
          tone: String(flags.tone || "").trim(),
          autoBuild: true,
        },
        kind: "auto-build",
        source: "auto-build",
        phase: "queued auto-build",
      });
      if (body.autorun !== false) {
        store.setRunning(true);
        runner.tick();
      }
      bus.emit();
      sendJson(res, 200, job);
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/launch-batch") {
      const body = await readBody(req);
      store.updateSettings(body.settings || {});
      const prompt = String(body.prompt || "").trim();
      const job = store.addJobWithMeta({
        flags: {
          prompt,
          brainstormSeeds: true,
          count: Number(body.count || 5),
          ideaLoop: Boolean(body.ideaLoop),
        },
        kind: "batch",
        source: "brainstorm",
        phase: "queued batch",
      });
      if (body.autorun !== false) {
        store.setRunning(true);
        runner.tick();
      }
      bus.emit();
      sendJson(res, 200, job);
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/start") {
      store.setRunning(true);
      runner.tick();
      bus.emit();
      sendJson(res, 200, store.snapshot(repo));
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/stop") {
      runner.stopLaunching();
      sendJson(res, 200, store.snapshot(repo));
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/hard-stop") {
      runner.hardStop();
      sendJson(res, 200, store.snapshot(repo));
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/retry") {
      const body = await readBody(req);
      const job = store.retryJob(body.id);
      bus.emit();
      sendJson(res, job ? 200 : 404, job || { error: "job not found" });
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/settings") {
      const body = await readBody(req);
      store.updateSettings(body);
      bus.emit();
      sendJson(res, 200, store.snapshot(repo));
      return;
    }
    if (req.method === "POST" && url.pathname === "/api/clear-complete") {
      store.clearComplete();
      bus.emit();
      sendJson(res, 200, store.snapshot(repo));
      return;
    }
    serveStatic(req, res);
  } catch (error) {
    sendJson(res, 500, { error: error.message });
  }
});

const port = Number(process.env.PORT || 4188);
server.listen(port, () => {
  console.log(`MiniArcadeControl listening on http://127.0.0.1:${port}`);
});
