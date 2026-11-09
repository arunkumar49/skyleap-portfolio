import { Link } from 'react-router'
import { links, profile } from '../../content/site.js'
import { navItems } from './navItems.js'
import './SiteFooter.css'

export default function SiteFooter() {
  const year = new Date().getFullYear()

  return (
    <footer className="site-footer">
      <div className="container site-footer__inner">
        <span className="site-footer__credit">
          Built by {profile.name} · {profile.locationShort} · © {year}
        </span>
        <div className="site-footer__links">
          {navItems.map((item) => (
            <Link key={item.to} to={item.to}>
              {item.label}
            </Link>
          ))}
          {links.linkedin && (
            <a href={links.linkedin} target="_blank" rel="noreferrer">
              LinkedIn ↗
            </a>
          )}
          {links.github && (
            <a href={links.github} target="_blank" rel="noreferrer">
              GitHub ↗
            </a>
          )}
        </div>
      </div>
    </footer>
  )
}
