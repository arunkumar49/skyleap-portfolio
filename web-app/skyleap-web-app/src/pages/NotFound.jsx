import { Link } from 'react-router'

export default function NotFound() {
  return (
    <section className="container not-found">
      <span className="eyebrow">/404</span>
      <h1 className="page-head__title">Page not found</h1>
      <p className="page-head__lede">The page you’re looking for doesn’t exist or has moved.</p>
      <div className="button-row">
        <Link to="/" className="btn btn--primary">
          Back to home
        </Link>
      </div>
    </section>
  )
}
