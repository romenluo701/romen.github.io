import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  breaks: false,
  typographer: false,
})

/** 渲染 Markdown 为 HTML 字符串（仅在服务端 / 构建期调用） */
export function renderMarkdown(src: string): string {
  if (!src) return ''
  return md.render(src)
}
