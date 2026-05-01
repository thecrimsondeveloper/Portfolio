import { getArcadePageHref, loadArcadeLibraryEntries, loadArcadeMetadataFromEntry } from "../data/arcade-projects.js";

let activePrototypeBookHost = null;
let activePrototypeBookPage = null;
let activeHydrationToken = 0;

function projectFromEntry(entry, metadata = null) {
  return {
    ...(metadata || {}),
    slug: entry.slug,
    pagePath: entry.pagePath,
    title: entry.title || metadata?.title || entry.slug,
    image: metadata?.image || "",
  };
}

async function loadSelectedProject(entries, forceReload = false) {
  const searchParams = new URLSearchParams(window.location.search);
  const selectedSlug = searchParams.get("prototype");
  const selectedEntry = entries.find((entry) => entry.slug === selectedSlug) || entries[0];
  if (!selectedEntry) return null;

  const metadata = await loadArcadeMetadataFromEntry(selectedEntry, forceReload);
  return projectFromEntry(selectedEntry, metadata);
}

function getEntryProjects(entries) {
  return entries.map((entry) => projectFromEntry(entry));
}

function handleArcadeRefreshClick(event) {
  const refreshButton = event.target instanceof HTMLElement ? event.target.closest("[data-arcade-refresh]") : null;
  if (!refreshButton) return;
  event.preventDefault();
  if (!activePrototypeBookHost || !activePrototypeBookPage) return;
  renderPrototypeBookView(activePrototypeBookHost, activePrototypeBookPage, true);
}

document.addEventListener("click", handleArcadeRefreshClick);

function buildArcadeHref(slug) {
  const searchParams = new URLSearchParams();
  searchParams.set("page", "prototypes");
  searchParams.set("prototype", slug);
  return `/?${searchParams.toString()}`;
}

function buildArcadeLibraryHref(slug) {
  const searchParams = new URLSearchParams();
  searchParams.set("page", "arcade-library");
  if (slug) {
    searchParams.set("prototype", slug);
  }
  return `/?${searchParams.toString()}`;
}

function getSelectedProject(prototypes) {
  const searchParams = new URLSearchParams(window.location.search);
  const selectedSlug = searchParams.get("prototype");
  return prototypes.find((project) => project.slug === selectedSlug) || prototypes[0];
}

const ARCADE_RECENT_STORAGE_KEY = "arcade-recent-games";

function readRecentArcadeSlugs() {
  try {
    const raw = window.localStorage.getItem(ARCADE_RECENT_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter((value) => typeof value === "string") : [];
  } catch {
    return [];
  }
}

function writeRecentArcadeSlugs(slugs) {
  try {
    window.localStorage.setItem(ARCADE_RECENT_STORAGE_KEY, JSON.stringify(slugs));
  } catch {
    // Ignore storage failures and keep the view functional.
  }
}

function updateRecentArcadeSlugs(currentSlug) {
  const recent = readRecentArcadeSlugs().filter((slug) => slug !== currentSlug);
  const nextRecent = [currentSlug, ...recent].slice(0, 4);
  writeRecentArcadeSlugs(nextRecent);
  return nextRecent;
}

function getRecentArcadeProjects(prototypes, currentSlug) {
  return updateRecentArcadeSlugs(currentSlug)
    .slice(1, 4)
    .map((slug) => prototypes.find((project) => project.slug === slug))
    .filter(Boolean);
}

function renderPrototypeIndexItem(project, isActive) {
  const coverMarkup = project.image
    ? `<img class="prototype-book-card-image" src="${project.image}" alt="${project.title}" loading="lazy" />`
    : `<div class="prototype-book-card-fallback" aria-hidden="true">Image</div>`;

  return `
    <a
      class="prototype-book-card${isActive ? " active" : ""}"
      href="${buildArcadeHref(project.slug)}"
      data-route-link
      data-arcade-card="${project.slug}"
      ${isActive ? 'aria-current="page"' : ""}
    >
      <div class="prototype-book-card-image-shell">
        ${coverMarkup}
      </div>
      <div class="prototype-book-card-label">
        <span class="prototype-book-card-title">${project.title}</span>
      </div>
    </a>
  `;
}

function renderArcadeRailItem(project, isActive) {
  const coverMarkup = project.image
    ? `<img class="arcade-rail-image" src="${project.image}" alt="${project.title}" loading="lazy" />`
    : `<div class="arcade-rail-fallback" aria-hidden="true">${project.title}</div>`;

  return `
    <a
      class="arcade-rail-card${isActive ? " active" : ""}"
      href="${buildArcadeHref(project.slug)}"
      data-route-link
      data-arcade-card="${project.slug}"
      ${isActive ? 'aria-current="page"' : ""}
    >
      ${coverMarkup}
      <span class="arcade-rail-overlay">
        <span class="arcade-rail-title">${project.title}</span>
      </span>
    </a>
  `;
}

function renderPrototypeFrame(project) {
  const href = project.pagePath || getArcadePageHref(project.slug);

  return `
    <div class="prototype-reader-shell">
      <div class="prototype-reader-frame-shell">
        <iframe
          class="prototype-reader-frame"
          src="${href}"
          title="${project.title}"
          loading="lazy"
          referrerpolicy="no-referrer"
        ></iframe>
      </div>
    </div>
  `;
}

function scheduleMetadataHydration(host, entries, forceReload, token) {
  const hydrate = async () => {
    const visibleCards = Array.from(host.querySelectorAll("[data-arcade-card]"));
    const visibleSlugs = new Set(visibleCards.map((card) => card.getAttribute("data-arcade-card")).filter(Boolean));
    const entriesToHydrate = entries.filter((entry) => visibleSlugs.has(entry.slug));

    await Promise.all(
      entriesToHydrate.map(async (entry) => {
        const metadata = await loadArcadeMetadataFromEntry(entry, forceReload);
        if (!metadata || token !== activeHydrationToken) return;
        const cards = host.querySelectorAll(`[data-arcade-card="${entry.slug}"]`);
        cards.forEach((card) => {
          const title = metadata.title || entry.title || entry.slug;
          const image = metadata.image;
          const fallback = card.querySelector(".prototype-book-card-fallback, .arcade-rail-fallback");
          if (image && fallback) {
            const img = document.createElement("img");
            img.src = image;
            img.alt = title;
            img.loading = "lazy";
            img.className = fallback.classList.contains("arcade-rail-fallback")
              ? "arcade-rail-image"
              : "prototype-book-card-image";
            fallback.replaceWith(img);
          }
        });
      })
    );
  };

  window.requestIdleCallback ? window.requestIdleCallback(hydrate, { timeout: 1500 }) : window.setTimeout(hydrate, 250);
}

async function renderArcadeMarkup(page, entries, forceReload = false) {
  const selectedProject = await loadSelectedProject(entries, forceReload);
  if (!selectedProject) {
    return "";
  }
  const prototypes = getEntryProjects(entries).map((project) =>
    project.slug === selectedProject.slug ? selectedProject : project
  );
  const recentProjects = getRecentArcadeProjects(prototypes, selectedProject.slug);
  const railMarkup = prototypes
    .map((project) => renderArcadeRailItem(project, project.slug === selectedProject.slug))
    .join("");
  const recentMarkup = recentProjects.length
    ? `
      <nav class="prototype-player-recent" aria-label="Recent arcade games">
        ${recentProjects
          .map(
            (project) => `
              <a class="prototype-player-crumb" href="${buildArcadeHref(project.slug)}" data-route-link>
                ${project.title}
              </a>
            `
          )
          .join("")}
      </nav>
    `
    : "";

  return `
    <div class="page-frame">
      <section class="content-section prototype-book prototype-book-player" aria-labelledby="prototype-book-heading">
        <div class="prototype-player-heading">
          <div class="prototype-player-heading-top">
            <a class="arcade-back-link" href="/" data-route-link aria-label="Back to landing">
              <span aria-hidden="true">←</span>
              <span>Start</span>
            </a>
            <h1 class="prototype-player-title" id="prototype-book-heading">${selectedProject.title}</h1>
            <div class="arcade-local-nav">
              <a class="button-link secondary" href="/?page=prototypes" data-route-link>Player</a>
              <a class="button-link secondary" href="/?page=arcade-library" data-route-link>Library</a>
            </div>
            <button type="button" class="button-link secondary" data-arcade-refresh>
              Refresh game list
            </button>
          </div>
          ${recentMarkup}
        </div>
        <div class="arcade-player-layout">
          <div class="prototype-book-reader" data-prototype-reader>${renderPrototypeFrame(selectedProject)}</div>
          <aside class="arcade-rail" aria-label="Arcade games">
            ${railMarkup}
          </aside>
        </div>
      </section>
    </div>
  `;
}

async function renderArcadeLibraryMarkup(page, entries, forceReload = false) {
  const prototypes = getEntryProjects(entries);
  const selectedEntryProject = getSelectedProject(prototypes);
  const selectedEntry = entries.find((entry) => entry.slug === selectedEntryProject?.slug) || entries[0];
  const selectedProject = selectedEntry ? projectFromEntry(selectedEntry) : selectedEntryProject;
  const indexMarkup = prototypes
    .map((project) => renderPrototypeIndexItem(project, project.slug === selectedProject?.slug))
    .join("");

  return `
    <div class="page-frame">
      <section class="section-header">
        <h1 class="section-heading">${page.title}</h1>
        <p class="section-subtitle">${page.subtitle}</p>
      </section>

      <section class="content-section prototype-book" aria-labelledby="prototype-book-heading">
        <div class="content-section-header">
          <div>
            <h2 class="content-section-title" id="prototype-book-heading">Arcade Library</h2>
          </div>
          <div class="arcade-local-nav">
            <a class="button-link secondary" href="/?page=prototypes" data-route-link>Player</a>
            <a class="button-link secondary" href="/?page=arcade-library" data-route-link>Library</a>
          </div>
          <button type="button" class="button-link secondary" data-arcade-refresh>
            Refresh game list
          </button>
        </div>

        <div class="prototype-library-note">
          <h3>${selectedProject.title}</h3>
          <p>Browse the gallery here, then launch the selected game in the Arcade player.</p>
          <a class="button-link primary" href="${buildArcadeHref(selectedProject.slug)}" data-route-link>
            Launch In Arcade
          </a>
        </div>

        <aside class="prototype-book-grid" aria-label="Arcade library">
          ${indexMarkup}
        </aside>
      </section>
    </div>
  `;
}

export async function renderPrototypeBookView(host, page, forceReload = false) {
  activePrototypeBookHost = host;
  activePrototypeBookPage = page;
  const hydrationToken = ++activeHydrationToken;

  host.innerHTML = `
    <div class="page-frame">
      <section class="content-section">
        <p>Loading arcade metadata…</p>
      </section>
    </div>
  `;

  const entries = await loadArcadeLibraryEntries(forceReload);
  const output =
    page.id === "arcade-library"
      ? await renderArcadeLibraryMarkup(page, entries, forceReload)
      : await renderArcadeMarkup(page, entries, forceReload);

  host.innerHTML = output;
  if (page.id !== "arcade-library") {
    scheduleMetadataHydration(host, entries, forceReload, hydrationToken);
  }

  if (forceReload) {
    // keep the latest page so refresh remains active after the reload.
    activePrototypeBookHost = host;
    activePrototypeBookPage = page;
  }
}
