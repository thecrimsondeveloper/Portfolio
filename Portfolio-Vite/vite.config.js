import { cpSync, existsSync, readdirSync, rmSync } from "node:fs";
import { extname, resolve } from "node:path";
import { defineConfig } from "vite";

const pageEntries = Object.fromEntries(
  readdirSync(resolve(__dirname, "Pages"))
    .filter((file) => extname(file) === ".html")
    .map((file) => [file.replace(/\.html$/, ""), resolve(__dirname, "Pages", file)])
);

export default defineConfig({
  plugins: [
    {
      name: "copy-arcade-pages",
      closeBundle() {
        const source = resolve(__dirname, "Pages");
        const destination = resolve(__dirname, "dist", "Pages");
        if (!existsSync(source)) return;
        rmSync(destination, { recursive: true, force: true });
        cpSync(source, destination, { recursive: true });
      },
    },
  ],
  build: {
    rollupOptions: {
      input: {
        index: resolve(__dirname, "index.html"),
        ...pageEntries,
      },
    },
  },
});
