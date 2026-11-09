import { useMemo } from 'react'
import './PatchGrid.css'

/*
 * Illustrative "attention map": a grid of squares whose opacity comes from a few Gaussian blobs
 * plus seeded noise, with one highlighted query patch. Ported from the mockups' DCLogic code;
 * the seed makes the pattern identical on every render.
 */
function buildPatches({ cols, rows, blobs, seed, query, minOpacity }) {
  let state = seed
  const rnd = () => {
    state = (state * 16807) % 2147483647
    return state / 2147483647
  }

  const patches = []
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      let v = 0
      for (const b of blobs) {
        v += b.w * Math.exp(-((c - b.x) ** 2 + (r - b.y) ** 2) / (2 * b.s * b.s))
      }
      v = Math.min(1, v + rnd() * 0.1)
      const isQuery = c === query.c && r === query.r
      patches.push({
        key: `${r}-${c}`,
        isQuery,
        opacity: isQuery ? 1 : Number((minOpacity + (1 - minOpacity) * v).toFixed(2)),
      })
    }
  }
  return patches
}

export default function PatchGrid({ cols, rows, blobs, seed, query, minOpacity = 0.07 }) {
  const patches = useMemo(
    () => buildPatches({ cols, rows, blobs, seed, query, minOpacity }),
    [cols, rows, blobs, seed, query, minOpacity],
  )

  return (
    <div className="patch-grid" style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }} aria-hidden="true">
      {patches.map((p) => (
        <div
          key={p.key}
          className={p.isQuery ? 'patch-grid__cell patch-grid__cell--query' : 'patch-grid__cell'}
          style={{ opacity: p.opacity }}
        />
      ))}
    </div>
  )
}
