import { portfolioSchema } from "../data/portfolio.js";
import {
  applyFontFamily,
  applyStructurePadding,
  applyStructureRoundness,
  applyUiScale,
  DEFAULT_FONT_FAMILY,
  DEFAULT_STRUCTURE_PADDING,
  DEFAULT_STRUCTURE_ROUNDNESS,
  DEFAULT_UI_SCALE,
} from "../preferences.js";
import { applyTheme, DEFAULT_THEME } from "../themes.js";
import { createAppState, setMenuOpen, updateRoute } from "./state.js";
import { DEFAULT_PAGE_ID, resolveRoute } from "./router.js";
import { renderProjectMissing, renderProjectView } from "../ui/project-view.js";
import { renderConnectView } from "../ui/connect-view.js";
import { renderPrototypeBookView } from "../ui/prototype-book-view.js";
import { renderEmptySectionView, renderSectionView } from "../ui/section-view.js";
import { renderShell, applyDesignSchema } from "../ui/shell.js";
import { clearOverlay } from "../ui/overlay-root.js";
import { initParticles } from "../ui/particles.js";
import { initInteractiveMotion } from "../ui/motion.js";
import { renderSettingsView } from "../ui/settings-view.js";
import { cleanupLandingView, renderLandingView } from "../ui/landing-view.js";
import { initStarHud } from "../ui/star-hud.js";

export function startApp() {
  document.addEventListener("DOMContentLoaded", async () => {
    applyDesignSchema(portfolioSchema.design);

    const hosts = {
      header: document.querySelector("[data-app-header]"),
      overlay: document.querySelector("[data-app-overlay]"),
      particles: document.querySelector("[data-app-particles]"),
      sidebar: document.querySelector("[data-app-sidebar]"),
      main: document.querySelector("[data-app-main]"),
    };

    const route = resolveRoute(new URLSearchParams(window.location.search), portfolioSchema);
    const state = createAppState(
      portfolioSchema,
      route,
      DEFAULT_UI_SCALE,
      DEFAULT_FONT_FAMILY,
      DEFAULT_STRUCTURE_PADDING,
      DEFAULT_STRUCTURE_ROUNDNESS
    );

    applyTheme(DEFAULT_THEME);
    applyUiScale(DEFAULT_UI_SCALE);
    applyFontFamily(DEFAULT_FONT_FAMILY);
    applyStructurePadding(DEFAULT_STRUCTURE_PADDING);
    applyStructureRoundness(DEFAULT_STRUCTURE_ROUNDNESS);
    initStarHud(document.body);
    await renderApp(hosts, state);
    bindInteractions(hosts, state);
    initParticles(hosts.particles);
    initInteractiveMotion(document);
  });
}

async function renderApp(hosts, state) {
  clearOverlay(hosts.overlay);
  renderShell(hosts, state);
  document.body.classList.toggle("menu-open", state.menuOpen);

  if (state.route.type === "project") {
    cleanupLandingView();
    const project = state.schema.projects[state.route.projectSlug];
    if (!project) {
      renderProjectMissing(hosts.main, state.schema.profile.name);
      return;
    }

    const page = state.schema.pages[project.section] || state.schema.pages[DEFAULT_PAGE_ID];
    updateDocumentMeta(page.description, state.schema.profile.name);
    renderProjectView(hosts.main, project, page, state.schema.profile.name);
    return;
  }

  const page = state.schema.pages[state.route.pageId] || state.schema.pages[DEFAULT_PAGE_ID];
  updateDocumentMeta(page.description, state.schema.profile.name, page.title);

  if (page.type === "landing") {
    await renderLandingView(hosts.main, page, state.schema.profile);
    return;
  }

  cleanupLandingView();

  if (page.type === "settings") {
    renderSettingsView(hosts.main, page, state.schema.profile);
    return;
  }

  if (page.type === "connect") {
    renderConnectView(hosts.main, page, state.schema.profile);
    return;
  }

  if (page.id === "prototypes") {
    await renderPrototypeBookView(hosts.main, page, state.schema);
    return;
  }

  if (page.type === "empty") {
    renderEmptySectionView(hosts.main, page);
    return;
  }

  renderSectionView(hosts.main, page, state.schema);
}

function updateDocumentMeta(description, profileName, title = null) {
  document.title = `${title || "Portfolio"} | ${profileName}`;
  const descriptionTag = document.querySelector('meta[name="description"]');
  if (descriptionTag) {
    descriptionTag.setAttribute("content", description);
  }
}

function bindInteractions(hosts, state) {
  document.addEventListener("click", (event) => {
    const routeLink = event.target instanceof HTMLElement ? event.target.closest("[data-route-link]") : null;
    if (!(routeLink instanceof HTMLAnchorElement)) return;

    event.preventDefault();
    navigateTo(routeLink.getAttribute("href"), hosts, state);
  });

  document.addEventListener("click", (event) => {
    const toggle = event.target instanceof HTMLElement ? event.target.closest("[data-menu-toggle]") : null;
    if (!(toggle instanceof HTMLElement)) return;

    setMenuOpen(state, !state.menuOpen);
    renderApp(hosts, state);
  });

  window.addEventListener("popstate", () => {
    updateRoute(state, resolveRoute(new URLSearchParams(window.location.search), state.schema));
    setMenuOpen(state, false);
    renderApp(hosts, state);
  });
}

function navigateTo(href, hosts, state) {
  if (!href) return;
  window.history.pushState({}, "", href);
  updateRoute(state, resolveRoute(new URLSearchParams(window.location.search), state.schema));
  setMenuOpen(state, false);
  renderApp(hosts, state);
}
