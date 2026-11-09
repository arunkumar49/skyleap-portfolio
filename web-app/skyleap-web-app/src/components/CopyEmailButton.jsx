import { useEffect, useState } from 'react'

/**
 * Copies the email to the clipboard and shows "Copied ✓" for 2 seconds.
 * Falls back to opening the mail app when the Clipboard API is unavailable (e.g. non-HTTPS).
 */
export default function CopyEmailButton({ email, className, children }) {
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (!copied) return undefined
    const timer = setTimeout(() => setCopied(false), 2000)
    return () => clearTimeout(timer)
  }, [copied])

  async function handleClick() {
    try {
      await navigator.clipboard.writeText(email)
      setCopied(true)
    } catch {
      window.location.href = `mailto:${email}`
    }
  }

  return (
    <button type="button" className={className} onClick={handleClick}>
      <span aria-live="polite">{copied ? 'Copied ✓' : children}</span>
    </button>
  )
}
