import { useCallback, useEffect, useState } from 'react'

// Keep in sync with the inline script in index.html.
const STORAGE_KEY = 'skyleap-theme'

function readInitialTheme() {
  // index.html already resolved saved/system preference before first paint.
  const fromDom = document.documentElement.dataset.theme
  if (fromDom === 'light' || fromDom === 'dark') return fromDom
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

/**
 * Light/dark theme stored on <html data-theme>.
 * Only an explicit toggle is saved, so visitors who never toggle keep following their system setting.
 */
export function useTheme() {
  const [theme, setTheme] = useState(readInitialTheme)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
  }, [theme])

  const toggleTheme = useCallback(() => {
    setTheme((current) => {
      const next = current === 'dark' ? 'light' : 'dark'
      try {
        localStorage.setItem(STORAGE_KEY, next)
      } catch {
        // Storage blocked (e.g. private mode): theme still switches, just isn't remembered.
      }
      return next
    })
  }, [])

  return { theme, toggleTheme }
}
