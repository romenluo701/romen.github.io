import { loadSiteConfig, loadPost, loadPostList } from '../../../lib/data'
import { renderMarkdown } from '../../../lib/markdown'

export { data }
export type Data = Awaited<ReturnType<typeof data>>

async function data(pageContext: any) {
  const { slug } = pageContext.routeParams as { slug: string }
  const config = loadSiteConfig()
  const post = loadPost(slug)
  return {
    config,
    post: {
      ...post,
      html: renderMarkdown(post.markdown),
    },
    labelColorDict: loadPostList().labelColorDict,
  }
}
