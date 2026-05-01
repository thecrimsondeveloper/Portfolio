export function getArcadePageHref(slug) {
  return `Pages/${slug}/`;
}

export async function loadArcadeLibraryEntries(forceReload = false) {
  const manifestPath = new URL("Pages/arcade-library.json", window.location.origin);
  if (forceReload) {
    manifestPath.searchParams.set("t", Date.now().toString());
  }
  const response = await fetch(manifestPath.toString(), { cache: forceReload ? "reload" : "default" });
  if (!response.ok) {
    throw new Error(`Unable to load arcade library manifest: ${response.status}`);
  }
  const manifest = await response.json();
  return manifest.entries || manifest;
}

export async function loadArcadeMetadataFromEntry(entry, forceReload = false) {
  const metadataPath = entry.metadataPath || `${entry.pagePath || getArcadePageHref(entry.slug)}${entry.slug}.json`;
  const metadataUrl = new URL(metadataPath, window.location.origin);
  if (forceReload) {
    metadataUrl.searchParams.set("t", Date.now().toString());
  }
  const response = await fetch(metadataUrl.toString(), { cache: forceReload ? "reload" : "default" });
  if (!response.ok) {
    return null;
  }
  return response.json();
}
