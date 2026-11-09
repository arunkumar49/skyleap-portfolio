import './SectionHeading.css'

/** Section title with the mockup's heavy bottom rule. `aside` renders on the right. */
export default function SectionHeading({ id, children, aside }) {
  return (
    <div className="section-heading">
      <h2 id={id} className="section-heading__title">
        {children}
      </h2>
      {aside && <span className="section-heading__aside">{aside}</span>}
    </div>
  )
}
