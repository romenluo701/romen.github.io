<template>
  <li>
    <a class="post-card" :href="postUrl">
      <span class="post-card-title">{{ post.title }}</span>
      <span class="post-card-meta">
        <span
          v-for="label in post.labels"
          :key="label"
          class="tag-pill"
          :style="{ background: labelColor(label) }"
        >
          {{ label }}
        </span>
        <span class="tag-date">{{ post.createdAt }}</span>
      </span>
    </a>
  </li>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { link } from '../lib/site'

const props = defineProps<{
  post: { slug: string; title: string; labels: string[]; createdAt: string }
  labelColorDict: Record<string, string>
}>()

const postUrl = computed(() => link('post/' + props.post.slug))

function labelColor(label: string): string {
  return props.labelColorDict[label] || '#6b7280'
}
</script>
