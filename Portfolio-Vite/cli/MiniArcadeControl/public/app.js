const state = {
  snapshot: null,
  selectedJob: null,
};

const els = {
  repoStatus: document.querySelector("#repoStatus"),
  queueStatus: document.querySelector("#queueStatus"),
  counts: document.querySelector("#counts"),
  queueLane: document.querySelector("#queueLane"),
  drawer: document.querySelector("#drawer"),
  drawerTitle: document.querySelector("#drawerTitle"),
  drawerBody: document.querySelector("#drawerBody"),
  retryBtn: document.querySelector("#retryBtn"),
};

const api = async (path, body = {}) => {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return response.json();
};

const batchPrompt = () => document.querySelector("#batchPrompt").value.trim();

const autoFlags = () => ({
  idea: document.querySelector("#idea").value.trim(),
  theme: document.querySelector("#theme").value.trim(),
  mechanic: document.querySelector("#mechanic").value.trim(),
  content: document.querySelector("#content").value.trim(),
  depth: document.querySelector("#depth").value,
});

const settings = () => ({
  concurrency: Number(document.querySelector("#concurrency").value || 5),
  mode: document.querySelector("#mode").value,
  tryFull: document.querySelector("#tryFull").checked,
});

const batchCount = () => Number(document.querySelector("#batchCount").value || 5);

function formatDuration(job) {
  const ms = job.durationMs || (job.startedAt ? Date.now() - Date.parse(job.startedAt) : 0);
  const seconds = Math.floor(ms / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function consoleLines(job) {
  const lines = [
    ...(job.stderrTail || []).map((line) => ({ kind: "stderr", line })),
    ...(job.stdoutTail || []).map((line) => ({ kind: "stdout", line })),
  ].filter((item) => item.line);
  return lines.slice(-8);
}

function card(job) {
  const el = document.createElement("article");
  el.className = `workerCard ${job.status}`;
  const lines = consoleLines(job);
  const batchLabel = escapeHtml(job.flags.prompt || "sample prompt");
  const title = job.kind === "batch"
    ? "brainstorm batch"
    : job.kind === "auto-build"
      ? job.flags.idea || "auto-build"
      : job.flags.idea || "arcade";
  const consoleHtml = lines.length
    ? lines
        .map(
          (item) =>
            `<div class="consoleLine ${item.kind}">${escapeHtml(item.line)}</div>`,
        )
        .join("")
    : `<div class="consoleLine muted">${escapeHtml(job.phase)}</div>`;
  el.innerHTML = `
    <div class="cardTop">
      <strong>${title}</strong>
      <span class="pill">${job.status}</span>
    </div>
    <div class="flags">
      ${job.kind === "batch"
        ? batchLabel
        : `${job.flags.theme || "auto"} / ${job.flags.mechanic || "auto"} / ${job.flags.depth || "full"}`}
    </div>
    <div class="cardMeta">
      <span class="pill">${job.phase}</span>
      <span class="pill">${formatDuration(job)}</span>
    </div>
    <div class="consolePane">
      <div class="consoleLabel">worker console</div>
      <div class="consoleBody">${consoleHtml}</div>
    </div>
  `;
  el.addEventListener("click", () => openDrawer(job));
  return el;
}

function render(snapshot) {
  state.snapshot = snapshot;
  els.repoStatus.textContent = snapshot.repo.ok ? snapshot.repo.root : snapshot.repo.message;
  els.queueStatus.textContent = snapshot.running ? "running" : "stopped";
  els.counts.textContent = `queued ${snapshot.counts.queued || 0} / running ${snapshot.counts.running || 0}`;
  document.querySelector("#concurrency").value = snapshot.settings.concurrency;
  document.querySelector("#mode").value = snapshot.settings.mode;
  document.querySelector("#tryFull").checked = Boolean(snapshot.settings.tryFull);

  replace(els.queueLane, snapshot.jobs);
}

function replace(target, jobs) {
  target.replaceChildren(...jobs.map(card));
}

function openDrawer(job) {
  state.selectedJob = job;
  els.drawer.classList.add("open");
  els.drawerTitle.textContent = `${job.kind === "batch" ? "brainstorm batch" : job.flags.idea || "arcade"} / ${job.status}`;
  els.drawerBody.textContent = JSON.stringify(
    {
      id: job.id,
      flags: job.flags,
      status: job.status,
      phase: job.phase,
      command: job.command,
      packetPath: job.packetPath,
      slug: job.slug,
      stdoutTail: job.stdoutTail,
      stderrTail: job.stderrTail,
      exitCode: job.exitCode,
    },
    null,
    2,
  );
  els.retryBtn.disabled = !["blocked", "failed"].includes(job.status);
}

async function syncSettings() {
  const snapshot = await api("/api/settings", settings());
  render(snapshot);
}

document.querySelector("#hardStopBtn").addEventListener("click", async () => render(await api("/api/hard-stop")));
document.querySelector("#clearBtn").addEventListener("click", async () => render(await api("/api/clear-complete")));
document.querySelector("#tryFull").addEventListener("change", syncSettings);
document.querySelector("#mode").addEventListener("change", syncSettings);
document.querySelector("#concurrency").addEventListener("change", syncSettings);
document.querySelector("#launchAutoBtn").addEventListener("click", async () => {
  await api("/api/launch-auto-build", {
    flags: autoFlags(),
    settings: settings(),
    autorun: true,
  });
});
document.querySelector("#launchBatchBtn").addEventListener("click", async () => {
  await api("/api/launch-batch", {
    prompt: batchPrompt(),
    count: batchCount(),
    ideaLoop: document.querySelector("#ideaLoop").checked,
    settings: settings(),
    autorun: true,
  });
});
document.querySelector("#closeDrawer").addEventListener("click", () => els.drawer.classList.remove("open"));
els.retryBtn.addEventListener("click", async () => {
  if (!state.selectedJob) return;
  await api("/api/retry", { id: state.selectedJob.id });
});

const events = new EventSource("/api/events");
events.onmessage = (event) => render(JSON.parse(event.data));
fetch("/api/status").then((response) => response.json()).then(render);
