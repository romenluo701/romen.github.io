import vue from '@vitejs/plugin-vue'
import vike from 'vike/plugin'
import type { UserConfig } from 'vite'

// GitHub Pages base 路径。
// 自定义域名（blog.romen.eu.cc）下站点根为 '/'，默认 '/'
// 若退回默认域名 romenluo701.github.io/romen.github.io，设为 '/romen.github.io/' 或 SITE_BASE 覆盖
const base = process.env.SITE_BASE ?? '/'

const config: UserConfig = {
  base,
  plugins: [vue(), vike()],
}

export default config
