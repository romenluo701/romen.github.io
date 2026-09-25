<template>
  <title>{{ title }}</title>
  <meta name="description" :content="description" />
  <link rel="icon" :href="avatar" />
  <meta property="og:title" :content="title" />
  <meta property="og:description" :content="description" />
  <meta property="og:type" :content="isPost ? 'article' : 'blog'" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vike-vue/useData'

const data = useData() as any

const config = computed(() => data?.config ?? { title: '博客', subTitle: '', avatarUrl: '' })
const isPost = computed(() => Boolean(data?.post))
const title = computed(() =>
  isPost.value ? `${data.post.title} - ${config.value.title}` : config.value.title,
)
const description = computed(() =>
  isPost.value ? data.post.description : config.value.subTitle,
)
const avatar = computed(() => config.value.avatarUrl)
</script>
