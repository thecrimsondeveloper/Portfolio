export function createAppState(
  schema,
  route,
  uiScale,
  fontFamily,
  structurePadding,
  structureRoundness
) {
  return {
    schema,
    route,
    uiScale,
    fontFamily,
    structurePadding,
    structureRoundness,
    menuOpen: false,
  };
}

export function updateRoute(state, route) {
  state.route = route;
}

export function setMenuOpen(state, isOpen) {
  state.menuOpen = isOpen;
}

export function setUiScale(state, uiScale) {
  state.uiScale = uiScale;
}

export function setFontFamily(state, fontFamily) {
  state.fontFamily = fontFamily;
}

export function setStructurePadding(state, structurePadding) {
  state.structurePadding = structurePadding;
}

export function setStructureRoundness(state, structureRoundness) {
  state.structureRoundness = structureRoundness;
}
