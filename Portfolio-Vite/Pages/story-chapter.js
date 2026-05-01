const bootstrapper = document.currentScript;
if (!bootstrapper) {
  throw new Error("Story chapter loader requires a script element.");
}
const configPath = bootstrapper.dataset.config;
if (!configPath) {
  throw new Error("Story chapter loader requires a data-config attribute.");
}

document.body.style.margin = "0";
document.body.style.minHeight = "100vh";
document.body.style.fontFamily = "Inter, system-ui, sans-serif";
document.body.style.background = "#090b14";
document.body.style.color = "#eef3ff";
document.body.style.display = "flex";
document.body.style.justifyContent = "center";
document.body.style.alignItems = "center";
document.body.style.padding = "1rem";
document.body.style.boxSizing = "border-box";

document.body.innerHTML = `
  <main class="story-shell" id="story-shell">
    <header class="story-header">
      <div>
        <h1 id="story-title">Loading...</h1>
        <p id="story-subtitle">Please wait while the story loads.</p>
      </div>
      <p class="story-instructions" id="story-instructions"></p>
    </header>
    <section class="story-card">
      <h2 id="node-title"></h2>
      <p id="node-text"></p>
      <div id="choice-list" class="choice-list"></div>
    </section>
    <footer class="story-footer">
      <p id="story-progress"></p>
      <button id="restart-button" class="story-button secondary hidden" type="button">Restart Story</button>
    </footer>
  </main>
`;

const style = document.createElement("style");
style.textContent = `
  .story-shell { width: min(960px, 100%); max-width: 960px; background: rgba(10, 14, 24, 0.96); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; box-shadow: 0 34px 88px rgba(0,0,0,0.45); padding: 28px; }
  .story-header { display: grid; gap: 1rem; margin-bottom: 1.5rem; }
  .story-header h1 { margin: 0; font-size: clamp(2rem, 3vw, 3rem); letter-spacing: -0.04em; }
  .story-header p { margin: 0; line-height: 1.6; color: #b8c2dd; }
  .story-instructions { margin-top: 1rem; padding: 1rem 1.1rem; background: rgba(82, 95, 142, 0.12); border-radius: 18px; color: #d6deff; font-size: 0.98rem; }
  .story-card { padding: 1.5rem; background: rgba(13, 18, 31, 0.96); border: 1px solid rgba(255,255,255,0.08); border-radius: 22px; }
  .story-card h2 { margin-top: 0; font-size: clamp(1.55rem, 2vw, 2.2rem); }
  .story-card p { font-size: 1rem; line-height: 1.8; color: #dfe7ff; }
  .choice-list { display: grid; gap: 0.85rem; margin-top: 1.5rem; }
  .choice-button { border: none; background: linear-gradient(135deg, #5b8cff 0%, #61d8ff 100%); color: #07101d; font-weight: 700; padding: 1rem 1.1rem; border-radius: 16px; cursor: pointer; text-align: left; box-shadow: 0 12px 28px rgba(18, 34, 75, 0.35); transition: transform 0.16s ease, filter 0.16s ease; }
  .choice-button:hover { transform: translateY(-1px); filter: brightness(1.04); }
  .story-footer { display: flex; justify-content: space-between; align-items: center; gap: 1rem; margin-top: 1.5rem; }
  .story-progress { margin: 0; color: #9ab0d2; }
  .story-button { border: none; border-radius: 999px; padding: 0.95rem 1.6rem; font-size: 1rem; font-weight: 700; cursor: pointer; background: #5b8cff; color: #081026; }
  .story-button.secondary { background: rgba(255,255,255,0.08); color: #eef3ff; }
  .hidden { display: none !important; }
  @media (max-width: 640px) { .story-shell { padding: 18px; } .story-card { padding: 1.25rem; } }
`;
document.head.appendChild(style);

const titleEl = document.getElementById("story-title");
const subtitleEl = document.getElementById("story-subtitle");
const instructionsEl = document.getElementById("story-instructions");
const nodeTitleEl = document.getElementById("node-title");
const nodeTextEl = document.getElementById("node-text");
const choiceListEl = document.getElementById("choice-list");
const progressEl = document.getElementById("story-progress");
const restartButton = document.getElementById("restart-button");

let config = null;
let currentKey = null;
let stepCount = 0;

function renderNode(key) {
  if (!config || !config.story) return;
  const node = config.story.nodes[key];
  if (!node) return;
  currentKey = key;
  stepCount += 1;
  nodeTitleEl.textContent = node.title || "Untitled Chapter";
  nodeTextEl.textContent = node.text || "...";
  choiceListEl.innerHTML = "";
  if (node.choices && node.choices.length > 0) {
    node.choices.forEach((choice) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "choice-button";
      button.textContent = choice.label;
      button.addEventListener("click", () => {
        if (choice.target) {
          renderNode(choice.target);
        }
      });
      choiceListEl.appendChild(button);
    });
    restartButton.classList.add("hidden");
  } else if (node.transition || node.outcome) {
    const outcome = document.createElement("div");
    outcome.style.marginTop = "1.4rem";
    outcome.style.padding = "1rem";
    outcome.style.background = "rgba(255,255,255,0.05)";
    outcome.style.borderRadius = "16px";
    outcome.innerHTML = `
      <p style="margin:0 0 0.75rem; color:#dfe7ff;">${node.outcome ? node.outcome.join(" ") : "This path leads deeper into the archive."}</p>
      <p style="margin:0; color:#a8b3d1;">${node.transition ? `This chapter connects to ${node.transition}.` : "End of the story chapter."}</p>
    `;
    choiceListEl.appendChild(outcome);
    restartButton.classList.remove("hidden");
  } else {
    restartButton.classList.remove("hidden");
  }
  progressEl.textContent = `Step ${stepCount} · ${config.title}`;
}

function resetStory() {
  stepCount = 0;
  renderNode(config.story.start);
}

restartButton.addEventListener("click", () => {
  resetStory();
});

async function loadConfig() {
  const response = await fetch(configPath);
  if (!response.ok) {
    titleEl.textContent = "Unable to load story.";
    instructionsEl.textContent = `Failed to load ${configPath}`;
    return;
  }
  config = await response.json();
  titleEl.textContent = config.title || "Story Chapter";
  subtitleEl.textContent = config.subtitle || "A story-driven arcade experience.";
  instructionsEl.textContent = config.instructions || "Choose wisely and replay when the chapter ends.";
  resetStory();
}

loadConfig();
