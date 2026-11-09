import { useState } from 'react'
import { Link } from 'react-router'
import ProjectVisual from '../components/ProjectVisual.jsx'
import { TagList } from '../components/Tag.jsx'
import { projects, research } from '../content/site.js'
import './Projects.css'

const ALL = 'All'

function buildFilters(items) {
  const counts = new Map()
  for (const p of items) counts.set(p.category, (counts.get(p.category) ?? 0) + 1)
  return [{ label: ALL, count: items.length }, ...[...counts].map(([label, count]) => ({ label, count }))]
}

const filters = buildFilters(projects)

function ProjectCard({ project, index }) {
  return (
    <article className="project-card">
      <ProjectVisual project={project} />
      <div className="project-card__body">
        <div className="project-card__meta">
          <span>{project.category}</span>
          <span>run/{String(index + 1).padStart(2, '0')}</span>
        </div>
        <h2 className="project-card__title">{project.title}</h2>
        <p className="project-card__summary">{project.summary}</p>
        <div className="project-card__tags">
          <TagList items={project.tags} />
        </div>
        {project.caseStudyUrl && (
          <a href={project.caseStudyUrl} className="project-card__link">
            Read case study →
          </a>
        )}
      </div>
    </article>
  )
}

export default function Projects() {
  const [active, setActive] = useState(ALL)
  const visible = active === ALL ? projects : projects.filter((p) => p.category === active)

  return (
    <>
      <section className="container projects-head">
        <div className="page-head">
          <div className="page-head__title-group">
            <span className="eyebrow">/projects</span>
            <h1 className="page-head__title">Projects</h1>
          </div>
          <p className="page-head__lede">
            A selection of my engineering work, spanning generative AI, computer vision and web applications.
          </p>
        </div>
        <div role="group" aria-label="Filter projects" className="filter-chips">
          {filters.map((f) => (
            <button
              key={f.label}
              type="button"
              className="filter-chip"
              aria-pressed={active === f.label}
              onClick={() => setActive(f.label)}
            >
              {f.label} · {f.count}
            </button>
          ))}
        </div>
      </section>

      <section aria-label="Engineering projects" className="container projects-grid-section">
        {visible.length > 0 ? (
          <div className="projects-grid">
            {visible.map((project) => (
              <ProjectCard key={project.id} project={project} index={projects.indexOf(project)} />
            ))}
          </div>
        ) : (
          <p className="projects-empty">No projects in this category yet.</p>
        )}
      </section>

      {research.length > 0 && (
        <section aria-labelledby="res-title" className="container research">
          <div className="research__head">
            <div className="page-head__title-group">
              <span className="eyebrow">/research</span>
              <h2 id="res-title" className="research__title">
                Research
              </h2>
            </div>
          </div>
          <div className="research__list">
            {research.map((item, i) => (
              <article key={item.id} className="research-item">
                <span className="research-item__index">R/{String(i + 1).padStart(2, '0')}</span>
                <div className="research-item__body">
                  <h3 className="research-item__title">{item.title}</h3>
                  <p className="research-item__text">{item.body}</p>
                </div>
                {item.focus?.length > 0 && (
                  <dl className="research-item__focus">
                    <dt>Key focus</dt>
                    <dd>
                      <TagList items={item.focus} />
                    </dd>
                  </dl>
                )}
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="container projects-cta-section">
        <div className="projects-cta">
          <p className="projects-cta__text">Have a problem that needs a vision model, a RAG system or a web app?</p>
          <Link to="/contact" className="btn projects-cta__btn">
            Start a conversation <span aria-hidden="true">→</span>
          </Link>
        </div>
      </section>
    </>
  )
}
