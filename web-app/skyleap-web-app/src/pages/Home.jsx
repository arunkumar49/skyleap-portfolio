import { Link } from 'react-router'
import CopyEmailButton from '../components/CopyEmailButton.jsx'
import PatchGrid from '../components/PatchGrid.jsx'
import { HERO_GRID } from '../components/patchGridPresets.js'
import { profile } from '../content/site.js'
import './Home.css'

export default function Home() {
  const intro = profile.heroIntro

  return (
    <div className="home">
      <section className="container home-hero">
        <div className="home-hero__top">
          <div className="home-hero__meta">
            <code className="home-hero__snippet">{profile.snippet}</code>
            <span className="status-pill">
              <span className="status-dot" aria-hidden="true" />
              {profile.status} · {profile.locationShort}, IST
            </span>
          </div>
          <h1 className="home-hero__name">{profile.name}</h1>
        </div>

        <div className="home-hero__body">
          <div className="home-hero__copy">
            <p className="home-hero__role">{profile.role}</p>
            <p className="home-hero__intro">
              {intro.before}
              <strong>{intro.highlight1}</strong>
              {intro.middle}
              <strong>{intro.highlight2}</strong>
              {intro.after}
            </p>
            <div className="button-row">
              <Link to="/projects" className="btn btn--primary">
                Explore projects <span aria-hidden="true">→</span>
              </Link>
              <Link to="/contact" className="btn btn--outline">
                Get in touch
              </Link>
            </div>
          </div>
          <figure className="home-hero__figure">
            <PatchGrid {...HERO_GRID} />
            <figcaption className="home-hero__caption">
              <span>fig. 1 — attention from one query patch across a scene</span>
              <span>illustrative · 24 × 9 patches</span>
            </figcaption>
          </figure>
        </div>
      </section>

      <section aria-labelledby="cta-title" className="home-cta">
        <div className="container home-cta__inner">
          <div className="home-cta__copy">
            <span className="eyebrow home-cta__eyebrow">/contact</span>
            <h2 id="cta-title" className="home-cta__title">
              Ready to innovate?
            </h2>
            <p className="home-cta__text">
              Let’s discuss how ML architectures, RAG and agentic workflows can solve your complex problems.
            </p>
          </div>
          <div className="button-row">
            <Link to="/contact" className="btn home-cta__btn">
              Start a conversation <span aria-hidden="true">→</span>
            </Link>
            <CopyEmailButton email={profile.email} className="home-cta__copy-btn">
              Copy {profile.email}
            </CopyEmailButton>
          </div>
        </div>
      </section>
    </div>
  )
}
