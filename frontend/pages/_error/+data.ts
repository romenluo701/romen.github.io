import { loadSiteConfig } from '../../lib/data'

export { data }
export type Data = Awaited<ReturnType<typeof data>>

async function data() {
  return { config: loadSiteConfig() }
}
