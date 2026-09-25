import { loadAllSlugs } from '../../../lib/data'

export { onBeforePrerenderStart }

async function onBeforePrerenderStart() {
  return loadAllSlugs().map((slug) => `/post/${slug}`)
}
