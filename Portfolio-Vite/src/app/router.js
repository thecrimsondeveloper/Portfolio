export const DEFAULT_PAGE_ID = "landing";
const PAGE_ALIASES = {
  xr: "game-dev",
};

export function buildPageHref(pageId) {
  return `/?page=${encodeURIComponent(pageId)}`;
}

export function buildProjectHref(slug) {
  return `/?project=${encodeURIComponent(slug)}`;
}

export function resolveRoute(searchParams, schema) {
  const projectSlug = searchParams.get("project");
  if (projectSlug && schema.projects[projectSlug]) {
    const project = schema.projects[projectSlug];
    return {
      type: "project",
      projectSlug,
      pageId: project.section,
      currentLabel: project.title,
    };
  }

  const pageId = searchParams.get("page") || DEFAULT_PAGE_ID;
  const resolvedPageId = PAGE_ALIASES[pageId] || pageId;
  const page = schema.pages[resolvedPageId] || schema.pages[DEFAULT_PAGE_ID];
  return {
    type: page.type,
    pageId: page.id,
    currentLabel: page.title,
  };
}
