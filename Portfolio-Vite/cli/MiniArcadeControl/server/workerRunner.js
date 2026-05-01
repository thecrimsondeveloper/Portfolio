import { extractResult, parseEventLine, runMiniArcade } from "./cliBridge.js";

const terminalStatuses = new Set(["validated", "built", "blocked", "failed"]);

export class WorkerRunner {
  constructor(store, repo, emit) {
    this.store = store;
    this.repo = repo;
    this.emit = emit;
    this.children = new Map();
    this.timer = setInterval(() => this.tick(), 1000);
  }

  tick() {
    for (const job of this.store.state.jobs) {
      if (job.status === "running" && job.startedAt) {
        this.store.updateJob(job.id, { durationMs: Date.now() - Date.parse(job.startedAt) });
      }
    }
    if (!this.store.state.running || !this.repo.ok) {
      this.emit();
      return;
    }
    const active = this.store.state.jobs.filter((job) => job.status === "running").length;
    const openSlots = Math.max(0, this.store.state.settings.concurrency - active);
    const nextJobs = this.store.state.jobs.filter((job) => job.status === "queued").slice(0, openSlots);
    for (const job of nextJobs) {
      this.startJob(job);
    }
    this.emit();
  }

  startJob(job) {
    const startedAt = new Date().toISOString();
    const outputLines = [];
    const errLines = [];
    this.store.updateJob(job.id, {
      status: "running",
      phase: "mini-orchestrator",
      startedAt,
      endedAt: null,
      stdoutTail: [],
      stderrTail: [],
    });
    const { child, command } = runMiniArcade(this.repo, job.flags, this.store.state.settings, (event) => {
      if (event.kind === "stdout") {
        outputLines.push(event.line);
        const parsed = parseEventLine(event.line);
        if (parsed) {
          this.handleCliEvent(job.id, parsed);
        }
        this.store.updateJob(job.id, {
          command: command.label,
          stdoutTail: outputLines.slice(-12),
          phase: event.line.includes("reconciled") ? "reconciled" : "running",
        });
      }
      if (event.kind === "stderr" || event.kind === "error") {
        errLines.push(event.line);
        this.store.updateJob(job.id, {
          command: command.label,
          stderrTail: errLines.slice(-12),
          phase: "stderr",
        });
      }
      if (event.kind === "close") {
        const result = extractResult([...outputLines, ...errLines]);
        const mode = job.flags.autoBuild ? "auto-build" : this.store.state.settings.tryFull ? "build" : this.store.state.settings.mode;
        const failed = event.code !== 0;
        const status = failed && result.autoStatus !== "built"
          ? "failed"
          : result.blocked
            ? "blocked"
            : mode === "build" || mode === "auto-build"
              ? "built"
              : mode === "plan-only"
                ? "validated"
                : "validated";
        this.store.updateJob(job.id, {
          status,
          phase: status,
          endedAt: new Date().toISOString(),
          exitCode: event.code,
          packetPath: result.packetPath,
          slug: result.slug,
          stdoutTail: outputLines.slice(-12),
          stderrTail: errLines.slice(-12),
        });
        if (job.kind === "batch" && ["failed", "blocked"].includes(status)) {
          this.settleOpenChildren(job.id, status);
        }
        this.children.delete(job.id);
      }
      this.emit();
    });
    this.children.set(job.id, child);
    this.store.updateJob(job.id, { command: command.label });
  }

  handleCliEvent(parentId, parsed) {
    if (parsed.type === "BATCH_START") {
      const current = this.store.findJob(parentId);
      this.store.updateJob(parentId, {
        kind: "batch",
        source: "brainstorm",
        batchId: parsed.payload.batchId,
        phase: "brainstorm",
        flags: {
          ...(current?.flags || {}),
          prompt: parsed.payload.prompt || current?.flags?.prompt || "",
        },
      });
      return;
    }
    if (parsed.type === "BRAINSTORM_RESULT") {
      this.store.updateJob(parentId, {
        batchId: parsed.payload.batchId,
        phase: `seeded ${parsed.payload.seeds.length}`,
      });
      return;
    }
    if (parsed.type === "CHILD_START") {
      const existing = this.store.state.jobs.find((job) => job.parentJobId === parentId && job.id === parsed.payload.jobId);
      if (!existing) {
        this.store.addJobWithMeta({
          kind: "run",
          source: "brainstorm",
          batchId: parsed.payload.batchId,
          parentJobId: parentId,
          status: "running",
          phase: "child running",
          flags: parsed.payload.flags,
        });
        const child = this.store.state.jobs[this.store.state.jobs.length - 1];
        child.id = parsed.payload.jobId;
        child.status = "running";
        child.phase = "child running";
        this.store.save();
      }
      return;
    }
    if (parsed.type === "CHILD_DONE") {
      const child = this.store.findJob(parsed.payload.jobId);
      if (child) {
        this.store.updateJob(parsed.payload.jobId, {
          status: parsed.payload.status,
          phase: parsed.payload.status,
          packetPath: parsed.payload.packetPath || child.packetPath,
          slug: parsed.payload.slug || child.slug,
          endedAt: new Date().toISOString(),
        });
      }
      return;
    }
    if (parsed.type === "BATCH_DONE") {
      this.store.updateJob(parentId, {
        phase: "batch complete",
      });
      return;
    }
    if (parsed.type === "AUTO_BUILD_BLOCKED") {
      this.store.updateJob(parentId, {
        phase: "auto-build blocked",
      });
      return;
    }
    if (parsed.type === "AUTO_BUILD_DONE") {
      this.store.updateJob(parentId, {
        phase: parsed.payload.status || "auto-build done",
        slug: parsed.payload.slug || "",
      });
    }
  }

  settleOpenChildren(parentId, status) {
    for (const child of this.store.state.jobs) {
      if (child.parentJobId === parentId && ["queued", "running"].includes(child.status)) {
        this.store.updateJob(child.id, {
          status,
          phase: `parent ${status}`,
          endedAt: new Date().toISOString(),
        });
      }
    }
  }

  stopLaunching() {
    this.store.setRunning(false);
    this.emit();
  }

  hardStop() {
    this.store.setRunning(false);
    for (const [id, child] of this.children) {
      child.kill("SIGTERM");
      const current = this.store.state.jobs.find((job) => job.id === id);
      this.store.updateJob(id, {
        status: terminalStatuses.has(current?.status) ? current.status : "blocked",
        phase: "stopped",
        endedAt: new Date().toISOString(),
      });
    }
    this.children.clear();
    for (const job of this.store.state.jobs) {
      if (["queued", "running"].includes(job.status)) {
        this.store.updateJob(job.id, {
          status: "blocked",
          phase: "stopped",
          endedAt: new Date().toISOString(),
        });
      }
    }
    this.emit();
  }
}
