<template>
  <div class="comments-wrap">
    <button
      v-if="state !== 'loaded'"
      class="comment-btn"
      type="button"
      :disabled="state === 'loading'"
      @click="open"
    >
      {{ state === 'loading' ? '加载中…' : '评论' }}
    </button>
    <div ref="commentsEl" id="comments"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue'

const props = defineProps<{ repo: string }>()

const commentsEl = ref<HTMLElement | null>(null)
const state = ref<'idle' | 'loading' | 'loaded'>('idle')
let timer: ReturnType<typeof setInterval> | null = null

function themeAttr(): string {
  const t = localStorage.getItem('meek_theme')
  if (t === 'dark') return 'dark-blue'
  if (t === 'light') return 'github-light'
  return 'preferred-color-scheme'
}

function open() {
  if (state.value !== 'idle' || !commentsEl.value) return
  state.value = 'loading'
  const s = document.createElement('script')
  s.src = 'https://utteranc.es/client.js'
  s.setAttribute('repo', props.repo)
  s.setAttribute('issue-term', 'title')
  s.setAttribute('theme', themeAttr())
  s.setAttribute('crossorigin', 'anonymous')
  s.async = true
  commentsEl.value.appendChild(s)

  timer = setInterval(() => {
    const frame = document.querySelector('.utterances-frame')
    if (frame) {
      state.value = 'loaded'
      if (timer) clearInterval(timer)
      timer = null
    }
  }, 200)
}

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>
