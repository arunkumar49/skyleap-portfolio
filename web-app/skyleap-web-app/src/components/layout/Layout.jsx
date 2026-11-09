import { useEffect } from 'react'
import { Outlet, useLocation } from 'react-router'
import SiteFooter from './SiteFooter.jsx'
import SiteHeader from './SiteHeader.jsx'
import './Layout.css'

export default function Layout() {
  const { pathname } = useLocation()

  // Client-side navigation keeps the scroll position; start each page at the top.
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="layout">
      <SiteHeader />
      <main className="layout__main">
        <Outlet />
      </main>
      <SiteFooter />
    </div>
  )
}
