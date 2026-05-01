import { buildPageHref } from "../app/router.js";

export function applyDesignSchema(design) {
  const shell = design.shell;
  const root = document.body;
  root.style.setProperty("--header-height", shell.headerHeight);
  root.style.setProperty("--sidebar-width-collapsed", shell.railCollapsedWidth);
  root.style.setProperty("--sidebar-item-height", shell.railItemHeight);
  root.style.setProperty("--sidebar-width-expanded", shell.railExpandedWidth);
  root.style.setProperty("--sidebar-width-mobile", shell.mobileRailWidth);
  root.style.setProperty("--content-padding-desktop", shell.contentPaddingDesktop);
  root.style.setProperty("--content-padding-mobile", shell.contentPaddingMobile);
}

export function renderShell(hosts, state) {
  const isArcadePlayer = state.route.pageId === "prototypes";
  const isLanding = state.route.pageId === "landing";
  document.body.classList.toggle("arcade-player-mode", isArcadePlayer);
  document.body.classList.toggle("landing-mode", isLanding);
  renderHeader(hosts.header, state);
  renderSidebar(hosts.sidebar);
  renderFloatingSettings(hosts.overlay, state);
}

function renderHeader(header, state) {
  if (state.route.pageId === "landing") {
    header.innerHTML = "";
    return;
  }

  const { profile, nav } = state.schema;
  const activePageId = state.route.pageId;
  const navMarkup = nav
    .filter((item) => item.id !== "settings")
    .map((item) => {
      const current = item.id === activePageId;
      return `
        <a
          class="header-tab-card"
          href="${buildPageHref(item.id)}"
          data-route-link
          data-wobble
          ${current ? 'aria-current="page"' : ""}
        >
          <span class="header-tab-icon" aria-hidden="true">${item.icon}</span>
          <span class="header-tab-label">${item.label}</span>
        </a>
      `;
    })
    .join("");

  header.innerHTML = `
    <div class="site-header-brand">
      <p class="site-header-name">${profile.name}</p>
      <p class="site-header-subtitle">${profile.title}</p>
    </div>
    <nav class="site-header-nav" aria-label="Primary">
      ${navMarkup}
    </nav>
  `;
}

function renderSidebar(sidebar) {
  sidebar.innerHTML = "";
}

function renderFloatingSettings(overlay, state) {
  if (state.route.pageId === "prototypes" || state.route.pageId === "landing") {
    overlay.innerHTML = "";
    return;
  }

  const settingsPage = state.schema.nav.find((item) => item.id === "settings");
  if (!settingsPage) {
    overlay.innerHTML = "";
    return;
  }

  const current = settingsPage.id === state.route.pageId;
  overlay.innerHTML = `
    <div class="app-floating-settings">
      <a
        class="floating-settings-button"
        href="${buildPageHref(settingsPage.id)}"
        data-route-link
        data-wobble
        aria-label="${settingsPage.label}"
        title="${settingsPage.label}"
        ${current ? 'aria-current="page"' : ""}
      >
        <span class="floating-settings-icon">${settingsPage.icon}</span>
      </a>
    </div>
  `;
}
