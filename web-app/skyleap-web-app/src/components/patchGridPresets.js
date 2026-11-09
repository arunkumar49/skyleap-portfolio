// Presets matching the two mockup grids (defined once so useMemo deps stay stable).
export const HERO_GRID = {
  cols: 24,
  rows: 9,
  seed: 11,
  query: { c: 6, r: 4 },
  minOpacity: 0.07,
  blobs: [
    { x: 6, y: 4, s: 2.6, w: 1.0 },
    { x: 16, y: 3, s: 2.2, w: 0.75 },
    { x: 13, y: 7, s: 1.8, w: 0.55 },
    { x: 21, y: 6, s: 1.4, w: 0.4 },
  ],
}

export const CARD_GRID = {
  cols: 16,
  rows: 7,
  seed: 23,
  query: { c: 5, r: 3 },
  minOpacity: 0.06,
  blobs: [
    { x: 5, y: 3, s: 2.0, w: 1.0 },
    { x: 11, y: 2, s: 1.8, w: 0.7 },
    { x: 10, y: 5, s: 1.4, w: 0.5 },
  ],
}
