import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

export function detectRepoRoot() {
  let current = here;
  while (current !== path.dirname(current)) {
    const root = path.resolve(current, "..", "..");
    const cliRoot = path.join(root, "Portfolio-Vite", "cli");
    const checks = [
      path.join(cliRoot, "mini_arcade_orchestrator_cli.py"),
      path.join(cliRoot, "arcade_builder_cli.py"),
      path.join(root, "Portfolio-Vite"),
    ];
    if (checks.every((item) => fs.existsSync(item))) {
      return {
        ok: true,
        root,
        cliRoot,
        miniCli: checks[0],
        arcadeCli: checks[1],
        viteRoot: checks[2],
        message: "Portfolio root detected",
      };
    }
    current = path.dirname(current);
  }
  return {
    ok: false,
    root: null,
    cliRoot: null,
    miniCli: null,
    arcadeCli: null,
    viteRoot: null,
    message: "Could not detect Portfolio root",
  };
}
