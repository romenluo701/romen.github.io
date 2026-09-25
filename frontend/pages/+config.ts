import vikeVue from 'vike-vue/config'
import type { Config } from 'vike/types'

// 反主题闪烁：在 head 最前端读取 localStorage 并设置 data-theme
const themeScript =
  "<script>try{var t=localStorage.getItem('meek_theme');if(t!=='light'&&t!=='dark'&&t!=='auto'){t='light'}document.documentElement.setAttribute('data-theme',t)}catch(e){document.documentElement.setAttribute('data-theme','light')}</script>"

export default {
  prerender: true,
  ssr: true,
  lang: 'zh-CN',
  extends: vikeVue,
  headHtmlBegin: themeScript,
} satisfies Config
