import vue from '@vitejs/plugin-vue'
import vike from 'vike/plugin'
import type { UserConfig } from 'vite'

// GitHub Pages 项目站点 base 路径（仓库 romenluo701/romen.github.io）
// 若改用自定义域名或 user 站点，改为 '/' 即可
const base = process.env.SITE_BASE ?? '/romen.github.io/'

const config: UserConfig = {
  base,
  plugins: [vue(), vike()],
}

export default config
