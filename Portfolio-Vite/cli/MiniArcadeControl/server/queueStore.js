import fs from "node:fs";
import path from "node:path";

const defaultState = {
  running: false,
  settings: {
    concurrency: 5,
    mode: "auto-build",
    tryFull: false,
  },
  jobs: [],
};

export class QueueStore {
  constructor(filePath) {
    this.filePath = filePath;
    this.state = this.load();
  }

  load() {
    if (!fs.existsSync(this.filePath)) {
      return structuredClone(defaultState);
    }
    try {
      return { ...structuredClone(defaultState), ...JSON.parse(fs.readFileSync(this.filePath, "utf8")) };
    } catch {
      return structuredClone(defaultState);
    }
  }

  save() {
    fs.mkdirSync(path.dirname(this.filePath), { recursive: true });
    const tmp = `${this.filePath}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, `${JSON.stringify(this.state, null, 2)}\n`);
    fs.renameSync(tmp, this.filePath);
  }

  snapshot(repo) {
    return {
      repo,
      running: this.state.running,
      settings: this.state.settings,
      jobs: this.state.jobs,
      counts: this.counts(),
    };
  }

  counts() {
    return this.state.jobs.reduce(
      (acc, job) => {
        acc[job.status] = (acc[job.status] || 0) + 1;
        return acc;
      },
      { queued: 0, running: 0, validated: 0, built: 0, blocked: 0, failed: 0 },
    );
  }

  addJob(flags) {
    const job = {
      id: `job-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      flags,
      status: "queued",
      phase: "queued",
      kind: "run",
      source: "manual",
      batchId: "",
      parentJobId: "",
      command: "",
      stdoutTail: [],
      stderrTail: [],
      packetPath: "",
      slug: "",
      exitCode: null,
      startedAt: null,
      endedAt: null,
      createdAt: new Date().toISOString(),
      durationMs: 0,
    };
    this.state.jobs.push(job);
    this.save();
    return job;
  }

  addJobWithMeta(meta = {}) {
    const job = this.addJob(meta.flags || {});
    Object.assign(job, {
      kind: meta.kind || job.kind,
      source: meta.source || job.source,
      batchId: meta.batchId || job.batchId,
      parentJobId: meta.parentJobId || job.parentJobId,
      phase: meta.phase || job.phase,
      status: meta.status || job.status,
    });
    this.save();
    return job;
  }

  updateSettings(settings) {
    const next = { ...this.state.settings, ...settings };
    next.concurrency = Math.max(1, Math.min(10, Number(next.concurrency) || 5));
    next.mode = ["auto-build", "plan-only", "validate", "build"].includes(next.mode) ? next.mode : "auto-build";
    next.tryFull = Boolean(next.tryFull);
    this.state.settings = next;
    this.save();
  }

  setRunning(value) {
    this.state.running = Boolean(value);
    this.save();
  }

  updateJob(id, patch) {
    const job = this.state.jobs.find((item) => item.id === id);
    if (!job) return null;
    Object.assign(job, patch);
    if (job.startedAt && !job.endedAt) {
      job.durationMs = Date.now() - Date.parse(job.startedAt);
    }
    this.save();
    return job;
  }

  findJob(id) {
    return this.state.jobs.find((item) => item.id === id) || null;
  }

  retryJob(id) {
    const job = this.state.jobs.find((item) => item.id === id);
    if (!job || !["blocked", "failed"].includes(job.status)) return null;
    Object.assign(job, {
      status: "queued",
      phase: "requeued",
      stdoutTail: [],
      stderrTail: [],
      packetPath: "",
      exitCode: null,
      startedAt: null,
      endedAt: null,
      durationMs: 0,
    });
    this.save();
    return job;
  }

  clearComplete() {
    this.state.jobs = this.state.jobs.filter((job) => !["validated", "built", "blocked", "failed"].includes(job.status));
    this.save();
  }
}
