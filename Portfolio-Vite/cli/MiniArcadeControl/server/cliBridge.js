import path from "node:path";
import { spawn } from "node:child_process";

export function buildCommand(repo, flags, settings) {
  const args = [repo.miniCli];
  if (flags.autoBuild || settings.mode === "auto-build") {
    args.push("--auto-build");
  }
  if (flags.prompt) {
    args.push("--prompt", flags.prompt);
  }
  for (const key of ["idea", "theme", "mode", "tone", "mechanic", "content", "depth"]) {
    if (flags[key]) {
      args.push(`--${key}`, flags[key]);
    }
  }
  if (!flags.autoBuild && flags.brainstormSeeds) {
    args.push("--brainstorm-seeds", "--count", String(flags.count || 5));
  }
  if (!flags.autoBuild && flags.ideaLoop) {
    args.push("--idea-loop");
  }
  const mode = settings.tryFull ? "build" : settings.mode;
  if (!flags.autoBuild && mode === "plan-only") args.push("--plan-only");
  if (!flags.autoBuild && mode === "validate") args.push("--validate");
  if (!flags.autoBuild && mode === "build") args.push("--validate", "--build");
  return {
    cmd: "python3",
    args,
    cwd: repo.root,
    label: `python3 ${args.map((arg) => (arg.includes(" ") ? JSON.stringify(arg) : arg)).join(" ")}`,
  };
}

export function runMiniArcade(repo, flags, settings, onEvent) {
  const command = buildCommand(repo, flags, settings);
  const child = spawn(command.cmd, command.args, {
    cwd: command.cwd,
    stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, PYTHONUNBUFFERED: "1" },
  });
  const append = (kind, chunk) => {
    const lines = chunk.toString().split(/\r?\n/).filter(Boolean);
    for (const line of lines) {
      onEvent({ kind, line });
    }
  };
  child.stdout.on("data", (chunk) => append("stdout", chunk));
  child.stderr.on("data", (chunk) => append("stderr", chunk));
  child.on("error", (error) => onEvent({ kind: "error", line: error.message }));
  child.on("close", (code) => onEvent({ kind: "close", code }));
  return { child, command };
}

export function parseEventLine(line) {
  const match = line.match(/^(BATCH_START|BRAINSTORM_RESULT|CHILD_START|CHILD_STATUS|CHILD_DONE|BATCH_DONE|AUTO_BUILD_BLOCKED|AUTO_BUILD_DONE)\s+(\{.*\})$/);
  if (!match) return null;
  try {
    return { type: match[1], payload: JSON.parse(match[2]) };
  } catch {
    return null;
  }
}

export function extractResult(lines) {
  const joined = lines.join("\n");
  const packetMatch = joined.match(/(\/[^\s]+arcade_packets\/[^\s]+_reply\.md)/);
  const validatedMatch = joined.match(/validated\s+([a-z0-9-]+)/i);
  const builtMatch = joined.match(/built\s+([a-z0-9-]+)/i);
  const autoMatch = joined.match(/AUTO_BUILD_DONE\s+(\{.*\})/);
  let autoPayload = null;
  if (autoMatch) {
    try {
      autoPayload = JSON.parse(autoMatch[1]);
    } catch {
      autoPayload = null;
    }
  }
  const blocked = /blocked:/i.test(joined);
  return {
    packetPath: packetMatch ? path.normalize(packetMatch[1]) : "",
    slug: autoPayload?.slug || builtMatch?.[1] || validatedMatch?.[1] || "",
    autoStatus: autoPayload?.status || "",
    blocked: blocked || autoPayload?.status === "blocked",
  };
}
