import './Tag.css'

/** Small mono label. variant: 'muted' (filled, for cards) | 'outline' (bordered, for skills). */
export default function Tag({ children, variant = 'muted' }) {
  return <span className={`tag tag--${variant}`}>{children}</span>
}

export function TagList({ items, variant }) {
  return (
    <div className="tag-list">
      {items.map((item) => (
        <Tag key={item} variant={variant}>
          {item}
        </Tag>
      ))}
    </div>
  )
}
