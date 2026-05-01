import { subscribe } from "../data/star-store.js";

let unsubscribe = null;

function renderCount(root, value) {
  const count = root.querySelector("[data-star-count]");
  if (!count) return;
  count.textContent = String(value);
  root.classList.remove("star-hud--pulse");
  window.requestAnimationFrame(() => root.classList.add("star-hud--pulse"));
}

function animateCaughtStar(root, detail) {
  if (!detail || typeof detail.clientX !== "number" || typeof detail.clientY !== "number") return;
  const target = root.getBoundingClientRect();
  const sparkle = document.createElement("span");
  sparkle.className = "star-hud-flyer";
  sparkle.textContent = "★";
  sparkle.style.setProperty("--star-start-x", `${detail.clientX}px`);
  sparkle.style.setProperty("--star-start-y", `${detail.clientY}px`);
  sparkle.style.setProperty("--star-end-x", `${target.left + target.width * 0.38}px`);
  sparkle.style.setProperty("--star-end-y", `${target.top + target.height * 0.5}px`);
  document.body.appendChild(sparkle);
  sparkle.addEventListener("animationend", () => sparkle.remove(), { once: true });
}

export function initStarHud(root = document.body) {
  const existing = document.querySelector("[data-star-hud]");
  if (existing) {
    existing.remove();
  }

  const hud = document.createElement("aside");
  hud.className = "star-hud";
  hud.dataset.starHud = "true";
  hud.setAttribute("aria-label", "Caught stars");
  hud.setAttribute("aria-live", "polite");
  hud.innerHTML = `
    <span class="star-hud-icon" aria-hidden="true">★</span>
    <span class="star-hud-count" data-star-count>0</span>
  `;
  root.appendChild(hud);

  if (unsubscribe) unsubscribe();
  unsubscribe = subscribe((value) => renderCount(hud, value));
  document.addEventListener("portfolio-star-caught", (event) => animateCaughtStar(hud, event.detail));
}
