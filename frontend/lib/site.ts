/** 站点 base 路径（与 vite.config.ts 的 base 保持一致），用于生成内部链接 */
export const SITE_BASE: string = import.meta.env.BASE_URL

/** 拼接站点内绝对路径，例如 link('tag') => '/romen.github.io/tag' */
export function link(path: string): string {
  const p = path.startsWith('/') ? path.slice(1) : path
  return SITE_BASE + p
}
