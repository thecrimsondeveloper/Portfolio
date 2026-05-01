export const STAR_STORAGE_KEY = "portfolio-star-count";

const listeners = new Set();

function readStoredStars() {
  try {
    const raw = window.localStorage.getItem(STAR_STORAGE_KEY);
    const parsed = Number.parseInt(raw || "0", 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
  } catch {
    return 0;
  }
}

function writeStoredStars(value) {
  try {
    window.localStorage.setItem(STAR_STORAGE_KEY, String(value));
  } catch {
    // Storage can fail in private or restricted contexts; keep the UI usable.
  }
}

function notify(value) {
  listeners.forEach((listener) => listener(value));
}

export function getStars() {
  return readStoredStars();
}

export function addStars(count = 1) {
  const nextValue = Math.max(0, getStars() + count);
  writeStoredStars(nextValue);
  notify(nextValue);
  return nextValue;
}

export function subscribe(listener) {
  listeners.add(listener);
  listener(getStars());
  return () => listeners.delete(listener);
}
