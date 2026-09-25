import { ref } from 'vue'

export type ThemeMode = 'light' | 'dark' | 'auto'

const STORAGE_KEY = 'meek_theme'
const ORDER: ThemeMode[] = ['light', 'dark', 'auto']

function readInitial(): ThemeMode {
  if (typeof document !== 'undefined') {
    const attr = document.documentElement.getAttribute('data-theme')
    if (attr === 'light' || attr === 'dark' || attr === 'auto') return attr
  }
  return 'light'
}

const mode = ref<ThemeMode>(readInitial())

function apply(next: ThemeMode) {
  mode.value = next
  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme', next)
  }
}

function cycle() {
  const idx = ORDER.indexOf(mode.value)
  const next = ORDER[(idx + 1) % ORDER.length]
  apply(next)
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, next)
  }
}

/** 供客户端首屏同步 localStorage（反主题闪烁脚本已在 +config 注入） */
function sync() {
  let saved: ThemeMode = 'light'
  if (typeof localStorage !== 'undefined') {
    const v = localStorage.getItem(STORAGE_KEY)
    if (v === 'light' || v === 'dark' || v === 'auto') saved = v
  }
  apply(saved)
}

export function useTheme() {
  return { mode, cycle, sync }
}
