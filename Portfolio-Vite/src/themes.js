export const THEME_STORAGE_KEY = "portfolio-theme";
export const DEFAULT_THEME = "slate";

export const themes = [
  {
    id: "slate",
    label: "Slate",
    description: "Muted teal accents on a grounded dark editorial canvas.",
    preview: ["#17232a", "#ff7a59"],
  },
  {
    id: "dawn",
    label: "Dawn",
    description: "Soft blue contrast over a dark twilight shell.",
    preview: ["#233246", "#3b7fd1"],
  },
  {
    id: "ember",
    label: "Ember",
    description: "Dark charcoal framing with a vivid ember accent and high contrast.",
    preview: ["#141416", "#ff6a3d"],
  },
  {
    id: "forest",
    label: "Forest",
    description: "Deep green tones with mossy highlights and a quieter technical mood.",
    preview: ["#10231a", "#7bc97f"],
  },
  {
    id: "midnight",
    label: "Midnight",
    description: "Blue-black panels with cyan accenting and a sharper futuristic edge.",
    preview: ["#0b1020", "#63d7ff"],
  },
];

export function normalizeThemeId(themeId) {
  return themes.some((theme) => theme.id === themeId) ? themeId : DEFAULT_THEME;
}

export function getStoredTheme() {
  try {
    return localStorage.getItem(THEME_STORAGE_KEY);
  } catch {
    return null;
  }
}

export function storeTheme(themeId) {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, themeId);
  } catch {
    // Ignore storage failures in private/incognito contexts.
  }
}

export function applyTheme(themeId) {
  const normalized = normalizeThemeId(themeId);
  document.body.dataset.theme = normalized;
  storeTheme(normalized);
  return normalized;
}
