import { existsSync, readFileSync } from 'node:fs'
import path from 'node:path'

export interface SiteConfig {
  title: string
  subTitle: string
  avatarUrl: string
  homeUrl: string
  repo: string
}

export interface PostMeta {
  slug: string
  title: string
  labels: string[]
  createdAt: string
  description: string
  top: number
}

export interface PostListData {
  posts: PostMeta[]
  labelColorDict: Record<string, string>
}

export interface PostData extends PostMeta {
  markdown: string
}

function resolveDataDir(): string {
  const candidates = [
    path.resolve(process.cwd(), 'data'),
    path.resolve(process.cwd(), 'frontend', 'data'),
  ]
  for (const c of candidates) {
    if (existsSync(path.join(c, 'config.json'))) return c
  }
  return candidates[0]
}

const DATA_DIR = resolveDataDir()

function readJson<T>(rel: string): T {
  const full = path.join(DATA_DIR, rel)
  return JSON.parse(readFileSync(full, 'utf-8')) as T
}

export function loadSiteConfig(): SiteConfig {
  return readJson<SiteConfig>('config.json')
}

export function loadPostList(): PostListData {
  return readJson<PostListData>('postList.json')
}

export function loadPost(slug: string): PostData {
  return readJson<PostData>(path.join('posts', `${slug}.json`))
}

export function loadAllSlugs(): string[] {
  return loadPostList().posts.map((p) => p.slug)
}
