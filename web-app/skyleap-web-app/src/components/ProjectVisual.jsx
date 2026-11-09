import PatchGrid from './PatchGrid.jsx'
import { CARD_GRID } from './patchGridPresets.js'
import './ProjectVisual.css'

function Box({ children, kind = 'plain' }) {
  return <span className={`pv-box pv-box--${kind}`}>{children}</span>
}

function Arrow() {
  return <span className="pv-arrow">→</span>
}

/* Pipeline diagram: top row → middle stages → bottom row (the mockup's agentic RAG card). */
function FlowVisual({ flow }) {
  return (
    <div className="pv pv--flow">
      <div className="pv-row">
        {flow.top.map((label) => (
          <Box key={label}>{label}</Box>
        ))}
        <Arrow />
      </div>
      <div className="pv-row pv-row--indent-1">
        {flow.middle.map((label) => (
          <Box key={label} kind="strong">
            {label}
          </Box>
        ))}
      </div>
      <div className="pv-row pv-row--indent-2">
        {flow.bottom.map((label, i) => (
          <span key={label} className="pv-row">
            <Arrow />
            <Box kind={i === flow.bottom.length - 1 ? 'solid' : 'plain'}>{label}</Box>
          </span>
        ))}
      </div>
    </div>
  )
}

/* Layered application diagram (the mockup's backend card, adapted to a web app stack). */
function LayersVisual() {
  return (
    <div className="pv pv--layers">
      <div className="pv-row">
        <span className="pv-label">ui</span>
        <Box kind="solid">React</Box>
        <Arrow />
        <Box kind="strong">REST API</Box>
      </div>
      <div className="pv-divider" />
      <div className="pv-row">
        <span className="pv-label">api</span>
        <Box kind="solid">.NET · C#</Box>
        <Arrow />
        <Box kind="strong">services</Box>
        <Arrow />
        <Box>data</Box>
      </div>
      <div className="pv-divider" />
      <div className="pv-row">
        <span className="pv-label">cloud</span>
        <Box>AWS</Box>
        <Box>Azure</Box>
      </div>
    </div>
  )
}

export default function ProjectVisual({ project }) {
  return (
    <div className="pv-frame" aria-hidden="true">
      {project.visual === 'flow' && <FlowVisual flow={project.flow} />}
      {project.visual === 'grid' && <PatchGrid {...CARD_GRID} />}
      {project.visual === 'layers' && <LayersVisual />}
    </div>
  )
}
