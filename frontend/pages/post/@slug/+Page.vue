<template>
  <article>
    <h1 class="post-title">{{ post.title }}</h1>
    <div class="post-meta">
      <span
        v-for="label in post.labels"
        :key="label"
        class="tag-pill"
        :style="{ background: labelColor(label) }"
      >
        {{ label }}
      </span>
      <span class="tag-date">{{ post.createdAt }}</span>
    </div>
    <div class="markdown-body post-body" v-html="post.html"></div>
    <CommentsButton :repo="config.repo" />
  </article>
</template>

<script setup lang="ts">
import { useData } from 'vike-vue/useData'
import CommentsButton from '../../../components/CommentsButton.vue'

const data = useData() as any
const post = data.post
const config = data.config
const labelColorDict = data.labelColorDict as Record<string, string>

function labelColor(label: string): string {
  return labelColorDict?.[label] || '#6b7280'
}
</script>
