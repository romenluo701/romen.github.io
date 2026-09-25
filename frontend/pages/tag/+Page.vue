<template>
  <div>
    <div class="site-header" style="border-bottom: none; margin-bottom: 8px">
      <h1 class="tag-page-title">标签 / 搜索</h1>
      <div class="search-box">
        <input
          ref="searchEl"
          v-model="query"
          class="search-input"
          type="search"
          placeholder="搜索标题…"
          aria-label="搜索标题"
        />
      </div>
    </div>

    <div class="tag-cloud">
      <button
        class="tag-pill"
        :style="{ background: activeTag === null ? '#000' : '#6b7280' }"
        @click="setTag(null)"
      >
        全部<span class="tag-count">{{ posts.length }}</span>
      </button>
      <button
        v-for="t in tags"
        :key="t.name"
        class="tag-pill"
        :style="{ background: t.color }"
        @click="setTag(t.name)"
      >
        {{ t.name }}<span class="tag-count">{{ t.count }}</span>
      </button>
    </div>

    <ul class="post-list">
      <PostCard
        v-for="post in filteredPosts"
        :key="post.slug"
        :post="post"
        :label-color-dict="labelColorDict"
      />
    </ul>
    <div v-if="filteredPosts.length === 0" class="empty-tip">没有找到相关文章</div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useData } from 'vike-vue/useData'
import PostCard from '../../components/PostCard.vue'

const data = useData() as any
const posts = data.postList.posts
const labelColorDict = data.postList.labelColorDict as Record<string, string>

const query = ref('')
const activeTag = ref<string | null>(null)
const searchEl = ref<HTMLInputElement | null>(null)

const tags = computed(() => {
  const map = new Map<string, number>()
  for (const p of posts) {
    for (const label of p.labels) {
      map.set(label, (map.get(label) || 0) + 1)
    }
  }
  return Array.from(map.entries())
    .sort((a, b) => b[1] - a[1])
    .map(([name, count]) => ({ name, count, color: labelColorDict[name] || '#6b7280' }))
})

const filteredPosts = computed(() => {
  const q = query.value.trim().toLowerCase()
  return posts.filter((p: any) => {
    const matchTag = activeTag.value === null || p.labels.includes(activeTag.value)
    const matchQuery = q === '' || p.title.toLowerCase().includes(q)
    return matchTag && matchQuery
  })
})

function setTag(tag: string | null) {
  activeTag.value = tag
  query.value = ''
}

onMounted(() => {
  const handler = (e: KeyboardEvent) => {
    const el = e.target as HTMLElement
    const typing = ['INPUT', 'TEXTAREA', 'SELECT'].includes(el?.tagName || '')
    if (e.key === '/' && !typing) {
      e.preventDefault()
      searchEl.value?.focus()
    }
  }
  document.addEventListener('keydown', handler)
})
</script>
