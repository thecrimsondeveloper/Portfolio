import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const dataPath = path.join(root, "src/data/portfolio/projects.js");
const outputDir = path.join(root, "public/images/projects");
const publicPrefix = "/images/projects";

const source = fs.readFileSync(dataPath, "utf8");
const projectsStart = source.indexOf("export const projects = {");
const projectsSource = source.slice(projectsStart);
const projectBlocks = [...projectsSource.matchAll(/\n    (["']?)([a-zA-Z0-9_-]+)\1: \{[\s\S]*?\n    \}/g)];

const paletteBySection = {
  "full-stack": ["#0f172a", "#2563eb", "#22c55e", "#e0f2fe"],
  "game-dev": ["#14121f", "#7c3aed", "#f97316", "#ecfeff"],
  prototypes: ["#101827", "#06b6d4", "#facc15", "#ecfeff"],
  "agentic-engineering": ["#111827", "#14b8a6", "#a855f7", "#f8fafc"],
};

function value(block, key) {
  return (block.match(new RegExp(`${key}:\\s*"([^"]*)"`)) || [])[1] || "";
}

function listValues(block, key) {
  const match = block.match(new RegExp(`${key}:\\s*\\[([\\s\\S]*?)\\]`));
  if (!match) return [];
  return [...match[1].matchAll(/"([^"]+)"/g)].map((item) => item[1]).slice(0, 4);
}

function escapeXml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function wrapText(text, maxChars, maxLines) {
  const words = text.split(/\s+/).filter(Boolean);
  const lines = [];
  let line = "";
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > maxChars && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
    if (lines.length === maxLines) break;
  }
  if (line && lines.length < maxLines) lines.push(line);
  if (words.join(" ").length > lines.join(" ").length && lines.length) {
    lines[lines.length - 1] = `${lines[lines.length - 1].replace(/[,.:\s]+$/, "")}...`;
  }
  return lines;
}

function iconFor(section, title) {
  if (section === "full-stack") return "M250 360h460v60H250zM310 450h340v44H310zM372 530h216v38H372zM300 250h360v74H300z";
  if (section === "agentic-engineering") return "M480 228l176 102v204L480 636 304 534V330zM480 304l-110 64v128l110 64 110-64V368z";
  if (/dragon|sky/i.test(title)) return "M245 498c76-78 142-120 214-132l-58-86 130 60 104-78-24 122 116 46-130 26c-42 88-124 146-242 174 24-42 35-78 32-108-38-2-86-10-142-24z";
  if (/orbit|comet|aurora/i.test(title)) return "M480 272a168 168 0 110 336 168 168 0 010-336zm0 78a90 90 0 100 180 90 90 0 000-180zm-250 88c52-84 190-150 342-164 154-14 284 32 318 106-70-38-180-56-304-44-158 14-294 68-356 102z";
  if (/harbor|tide|drift|sandstorm/i.test(title)) return "M220 520c80-42 156-42 236 0s156 42 236 0 156-42 236 0v86c-80-42-156-42-236 0s-156 42-236 0-156-42-236 0zM260 420h440l-92-132H352z";
  if (/grid|pulse|neural/i.test(title)) return "M280 260h120v120H280zM430 260h120v120H430zM580 260h120v120H580zM280 410h120v120H280zM430 410h120v120H430zM580 410h120v120H580z";
  if (/beacon|signal|relay|courier|runner|sprint|lane/i.test(title)) return "M235 548l490-306-108 250h126L252 790l108-250z";
  if (/lab|rift|phase/i.test(title)) return "M322 246h316l-74 170 112 62-160 230 26-180-142-58z";
  return "M280 300h400v280H280zM340 360h280v52H340zM340 452h168v52H340z";
}

function makeSvg(project) {
  const [bg, primary, accent, ink] = paletteBySection[project.section] || paletteBySection.prototypes;
  const titleLines = wrapText(project.title, 28, 3);
  const details = [project.kind, ...project.technologies].filter(Boolean).slice(0, 4);
  const glyph = iconFor(project.section, project.title);
  const chips = details
    .map((detail, index) => {
      const x = 72 + (index % 2) * 290;
      const y = 664 + Math.floor(index / 2) * 54;
      return `<g><rect x="${x}" y="${y}" width="248" height="34" rx="17" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.18)"/><text x="${x + 18}" y="${y + 23}" fill="${ink}" opacity="0.86" font-size="17" font-family="Inter, Arial, sans-serif">${escapeXml(detail)}</text></g>`;
    })
    .join("");
  const titleText = titleLines
    .map((line, index) => `<text x="72" y="${132 + index * 62}" fill="${ink}" font-size="48" font-weight="760" font-family="Inter, Arial, sans-serif">${escapeXml(line)}</text>`)
    .join("");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720" role="img" aria-labelledby="title desc">
  <title id="title">${escapeXml(project.title)} card artwork</title>
  <desc id="desc">Generated portfolio card image for ${escapeXml(project.title)}.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${bg}"/>
      <stop offset="0.58" stop-color="${primary}"/>
      <stop offset="1" stop-color="${accent}"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="38%" r="52%">
      <stop offset="0" stop-color="${accent}" stop-opacity="0.52"/>
      <stop offset="1" stop-color="${accent}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse">
      <path d="M64 0H0v64" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
    </pattern>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="26" stdDeviation="20" flood-color="#000" flood-opacity="0.35"/>
    </filter>
  </defs>
  <rect width="960" height="720" fill="url(#bg)"/>
  <rect width="960" height="720" fill="url(#grid)" opacity="0.7"/>
  <rect width="960" height="720" fill="url(#glow)"/>
  <path d="M0 576c154-52 256-42 392 12 158 62 306 62 568-20v152H0z" fill="rgba(0,0,0,0.25)"/>
  <g transform="translate(250 126)" opacity="0.26" filter="url(#shadow)">
    <path d="${glyph}" fill="${ink}"/>
  </g>
  <rect x="48" y="48" width="864" height="624" rx="28" fill="rgba(8,12,24,0.30)" stroke="rgba(255,255,255,0.22)"/>
  <text x="72" y="88" fill="${ink}" opacity="0.72" font-size="19" letter-spacing="3" font-family="Inter, Arial, sans-serif">${escapeXml(project.section.toUpperCase())}</text>
  ${titleText}
  <text x="72" y="576" fill="${ink}" opacity="0.74" font-size="22" font-family="Inter, Arial, sans-serif">${escapeXml(project.kind || "Portfolio Project")}</text>
  ${chips}
</svg>
`;
}

const updates = [];

for (const match of projectBlocks) {
  const block = match[0];
  if (value(block, "image") !== "") continue;
  const project = {
    slug: value(block, "slug") || match[2],
    title: value(block, "title") || match[2],
    section: value(block, "section") || "prototypes",
    kind: value(block, "kind") || "",
    technologies: listValues(block, "technologies"),
  };
  const fileName = `${project.slug}.svg`;
  const imagePath = `${publicPrefix}/${fileName}`;
  fs.writeFileSync(path.join(outputDir, fileName), makeSvg(project));
  updates.push({ slug: project.slug, imagePath });
}

let nextSource = source;
for (const { slug, imagePath } of updates) {
  const blockPattern = new RegExp(`(slug: "${slug}",[\\s\\S]*?\\n      image:) ""`);
  nextSource = nextSource.replace(blockPattern, `$1\n        "${imagePath}"`);
}

fs.writeFileSync(dataPath, nextSource);

console.log(`Generated ${updates.length} project card images.`);
for (const update of updates) {
  console.log(`${update.slug} -> ${update.imagePath}`);
}
