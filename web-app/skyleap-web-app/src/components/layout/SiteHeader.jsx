import { Link, NavLink } from 'react-router'
import { profile } from '../../content/site.js'
import ThemeToggle from '../ThemeToggle.jsx'
import { navItems } from './navItems.js'
import './SiteHeader.css'

export default function SiteHeader() {
  return (
    <header className="site-header">
      <nav aria-label="Primary" className="container site-header__nav">
        <Link to="/" className="site-header__brand">
          <span className="site-header__monogram" aria-hidden="true">
            {profile.initials}
          </span>
          <span className="site-header__name">{profile.name}</span>
        </Link>
        <div className="site-header__links">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} className="site-header__link">
              {item.label}
            </NavLink>
          ))}
          <ThemeToggle />
        </div>
      </nav>
    </header>
  )
}
