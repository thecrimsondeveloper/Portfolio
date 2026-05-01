export const UI_SCALE_STORAGE_KEY = "portfolio-ui-scale";
export const DEFAULT_UI_SCALE = 2;
export const SUPPORTED_UI_SCALES = [1, 2, 3];
export const FONT_FAMILY_STORAGE_KEY = "portfolio-font-family";
export const DEFAULT_FONT_FAMILY = "avenir";
export const SUPPORTED_FONT_FAMILIES = ["avenir", "lexend"];
export const STRUCTURE_PADDING_STORAGE_KEY = "portfolio-structure-padding";
export const DEFAULT_STRUCTURE_PADDING = "tight";
export const SUPPORTED_STRUCTURE_PADDINGS = ["tight", "compact", "relaxed"];
export const STRUCTURE_ROUNDNESS_STORAGE_KEY = "portfolio-structure-roundness";
export const DEFAULT_STRUCTURE_ROUNDNESS = "square";
export const SUPPORTED_STRUCTURE_ROUNDNESS = ["square", "soft", "rounded"];

export function normalizeUiScale(value) {
  const parsed = Number.parseInt(String(value), 10);
  return SUPPORTED_UI_SCALES.includes(parsed) ? parsed : DEFAULT_UI_SCALE;
}

export function normalizeFontFamily(value) {
  return SUPPORTED_FONT_FAMILIES.includes(String(value))
    ? String(value)
    : DEFAULT_FONT_FAMILY;
}

export function normalizeStructurePadding(value) {
  return SUPPORTED_STRUCTURE_PADDINGS.includes(String(value))
    ? String(value)
    : DEFAULT_STRUCTURE_PADDING;
}

export function normalizeStructureRoundness(value) {
  return SUPPORTED_STRUCTURE_ROUNDNESS.includes(String(value))
    ? String(value)
    : DEFAULT_STRUCTURE_ROUNDNESS;
}

export function getStoredUiScale() {
  try {
    return normalizeUiScale(localStorage.getItem(UI_SCALE_STORAGE_KEY));
  } catch {
    return DEFAULT_UI_SCALE;
  }
}

export function getStoredFontFamily() {
  try {
    return normalizeFontFamily(localStorage.getItem(FONT_FAMILY_STORAGE_KEY));
  } catch {
    return DEFAULT_FONT_FAMILY;
  }
}

export function storeUiScale(value) {
  try {
    localStorage.setItem(UI_SCALE_STORAGE_KEY, String(normalizeUiScale(value)));
  } catch {
    // Ignore storage failures in private/incognito contexts.
  }
}

export function storeFontFamily(value) {
  try {
    localStorage.setItem(FONT_FAMILY_STORAGE_KEY, normalizeFontFamily(value));
  } catch {
    // Ignore storage failures in private/incognito contexts.
  }
}

export function applyUiScale(value) {
  const normalized = normalizeUiScale(value);
  document.body.dataset.uiScale = String(normalized);
  document.body.style.setProperty("--project-grid-columns", String(normalized));
  storeUiScale(normalized);
  return normalized;
}

export function applyFontFamily(value) {
  const normalized = normalizeFontFamily(value);
  const fontFamilies = {
    avenir: '"Avenir Next", "Trebuchet MS", sans-serif',
    lexend: 'Lexend, "Avenir Next", "Trebuchet MS", sans-serif',
  };

  document.body.dataset.fontFamily = normalized;
  document.body.style.setProperty("--app-font-family", fontFamilies[normalized]);
  storeFontFamily(normalized);
  return normalized;
}

export function getStoredStructurePadding() {
  try {
    return normalizeStructurePadding(localStorage.getItem(STRUCTURE_PADDING_STORAGE_KEY));
  } catch {
    return DEFAULT_STRUCTURE_PADDING;
  }
}

export function storeStructurePadding(value) {
  try {
    localStorage.setItem(
      STRUCTURE_PADDING_STORAGE_KEY,
      normalizeStructurePadding(value)
    );
  } catch {
    // Ignore storage failures in private/incognito contexts.
  }
}

export function applyStructurePadding(value) {
  const normalized = normalizeStructurePadding(value);
  const presets = {
    tight: {
      gap: "0",
      padding: "0.85rem",
      paddingMobile: "0.75rem",
      controlPaddingInline: "0.65rem",
      controlPaddingBlock: "0.5rem",
      controlMinHeight: "3rem",
    },
    compact: {
      gap: "0.5rem",
      padding: "1rem",
      paddingMobile: "0.85rem",
      controlPaddingInline: "0.8rem",
      controlPaddingBlock: "0.6rem",
      controlMinHeight: "3.2rem",
    },
    relaxed: {
      gap: "1rem",
      padding: "1.3rem",
      paddingMobile: "1rem",
      controlPaddingInline: "0.95rem",
      controlPaddingBlock: "0.72rem",
      controlMinHeight: "3.5rem",
    },
  };
  const preset = presets[normalized];
  document.body.dataset.structurePadding = normalized;
  document.body.style.setProperty("--structure-gap", preset.gap);
  document.body.style.setProperty("--structure-padding", preset.padding);
  document.body.style.setProperty("--structure-padding-mobile", preset.paddingMobile);
  document.body.style.setProperty("--structure-control-padding-inline", preset.controlPaddingInline);
  document.body.style.setProperty("--structure-control-padding-block", preset.controlPaddingBlock);
  document.body.style.setProperty("--structure-control-min-height", preset.controlMinHeight);
  storeStructurePadding(normalized);
  return normalized;
}

export function getStoredStructureRoundness() {
  try {
    return normalizeStructureRoundness(localStorage.getItem(STRUCTURE_ROUNDNESS_STORAGE_KEY));
  } catch {
    return DEFAULT_STRUCTURE_ROUNDNESS;
  }
}

export function storeStructureRoundness(value) {
  try {
    localStorage.setItem(
      STRUCTURE_ROUNDNESS_STORAGE_KEY,
      normalizeStructureRoundness(value)
    );
  } catch {
    // Ignore storage failures in private/incognito contexts.
  }
}

export function applyStructureRoundness(value) {
  const normalized = normalizeStructureRoundness(value);
  const presets = {
    square: { lg: "0", md: "0", sm: "0", sidebar: "0", control: "0", pill: "0" },
    soft: { lg: "10px", md: "8px", sm: "6px", sidebar: "12px", control: "8px", pill: "999px" },
    rounded: { lg: "22px", md: "16px", sm: "12px", sidebar: "18px", control: "12px", pill: "999px" },
  };
  const preset = presets[normalized];
  document.body.dataset.structureRoundness = normalized;
  document.body.style.setProperty("--content-shell-radius-lg", preset.lg);
  document.body.style.setProperty("--content-shell-radius-md", preset.md);
  document.body.style.setProperty("--content-shell-radius-sm", preset.sm);
  document.body.style.setProperty("--sidebar-panel-radius", preset.sidebar);
  document.body.style.setProperty("--button-radius", preset.control);
  document.body.style.setProperty("--control-pill-radius", preset.pill);
  storeStructureRoundness(normalized);
  return normalized;
}
