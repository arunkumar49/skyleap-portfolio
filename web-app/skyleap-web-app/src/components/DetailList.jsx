import './DetailList.css'

/** Two-column label/value list. Rows whose value is empty are skipped. */
export default function DetailList({ items }) {
  const visible = items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '')

  return (
    <dl className="detail-list">
      {visible.map((item) => (
        <div key={item.label} className="detail-list__row">
          <dt className="detail-list__label">{item.label}</dt>
          <dd className="detail-list__value">{item.value}</dd>
        </div>
      ))}
    </dl>
  )
}
