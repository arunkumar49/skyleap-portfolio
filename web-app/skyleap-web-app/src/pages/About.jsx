import { Link } from 'react-router'
import DetailList from '../components/DetailList.jsx'
import SectionHeading from '../components/SectionHeading.jsx'
import { TagList } from '../components/Tag.jsx'
import { experience, links, personalDetails, profile, skillGroups, writing } from '../content/site.js'
import './About.css'

function DownloadIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 3v12M7 10l5 5 5-5M5 21h14" />
    </svg>
  )
}

function Elsewhere() {
  const items = [
    links.linkedin && { label: 'LinkedIn ↗', href: links.linkedin },
    links.github && { label: 'GitHub ↗', href: links.github },
  ].filter(Boolean)

  if (items.length === 0) return null
  return (
    <span className="about-elsewhere">
      {items.map((item) => (
        <a key={item.href} href={item.href} target="_blank" rel="noreferrer">
          {item.label}
        </a>
      ))}
    </span>
  )
}

export default function About() {
  const details = [
    ...personalDetails,
    { label: 'Email', value: <a href={`mailto:${profile.email}`}>{profile.email}</a> },
    { label: 'Elsewhere', value: <Elsewhere /> },
  ].filter((item) => item.label !== 'Elsewhere' || links.linkedin || links.github)

  return (
    <>
      <section className="container about-hero">
        <figure className="about-portrait">
          {links.portraitUrl ? (
            <img src={links.portraitUrl} alt={`Portrait of ${profile.name}`} className="about-portrait__img" />
          ) : (
            <div className="about-portrait__placeholder" aria-hidden="true">
              <span>{profile.initials}</span>
            </div>
          )}
          <figcaption className="about-portrait__caption">{profile.location}</figcaption>
        </figure>

        <div className="about-hero__copy">
          <span className="eyebrow">/about</span>
          <h1 className="about-hero__name">{profile.name}</h1>
          <p className="about-hero__role">
            {profile.role} · {profile.company}
          </p>
          <p className="about-hero__intro">{profile.aboutIntro}</p>
          <p className="about-hero__secondary">{profile.aboutSecondary}</p>
          <div className="button-row about-hero__actions">
            {links.resumeUrl && (
              <a href={links.resumeUrl} className="btn btn--primary" download>
                <DownloadIcon />
                Download résumé (PDF)
              </a>
            )}
            <Link to="/contact" className={links.resumeUrl ? 'btn btn--outline' : 'btn btn--primary'}>
              Get in touch
            </Link>
          </div>
        </div>
      </section>

      <section aria-labelledby="pd-title" className="container about-section">
        <SectionHeading id="pd-title">Personal details</SectionHeading>
        <DetailList items={details} />
      </section>

      <section aria-labelledby="sk-title" className="container about-section">
        <SectionHeading id="sk-title">Skills &amp; tools</SectionHeading>
        <div className="skill-groups">
          {skillGroups.map((group) => (
            <div key={group.title} className="skill-group">
              <h3 className="skill-group__title">{group.title}</h3>
              <TagList items={group.items} variant="outline" />
            </div>
          ))}
        </div>
      </section>

      <section aria-labelledby="ex-title" className="container about-section">
        <SectionHeading id="ex-title">Experience</SectionHeading>
        <ol className="timeline">
          {experience.map((item) => (
            <li key={`${item.period}-${item.role}`} className="timeline__item">
              <span className="timeline__period">{item.period}</span>
              <div className="timeline__body">
                <span className="timeline__role">
                  {item.role} <span className="timeline__company">· {item.company}</span>
                </span>
                <span className="timeline__summary">{item.summary}</span>
              </div>
            </li>
          ))}
        </ol>
      </section>

      {writing.length > 0 && (
        <section aria-labelledby="wr-title" className="container about-section">
          <SectionHeading id="wr-title">Writing</SectionHeading>
          <div className="writing-grid">
            {writing.map((post) => (
              <a key={post.id} href={post.url} className="writing-card">
                <span className="writing-card__meta">
                  <span>{post.category}</span>
                  <span>{post.date}</span>
                </span>
                <span className="writing-card__title">{post.title}</span>
                <span className="writing-card__summary">{post.summary}</span>
                <span className="writing-card__link">Read article →</span>
              </a>
            ))}
          </div>
        </section>
      )}
    </>
  )
}
