<template>
  <header class="site-header">
    <a class="site-brand" :href="home">
      <img class="site-avatar" :src="config.avatarUrl" alt="avatar" />
      <span class="site-title">{{ config.title }}</span>
    </a>
    <nav class="site-nav" aria-label="站点导航">
      <a class="icon-btn" :href="home" title="首页" aria-label="首页">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 10.5 12 3l9 7.5" />
          <path d="M5 9.5V21h14V9.5" />
        </svg>
      </a>
      <a class="icon-btn" :href="tagUrl" title="搜索 / 标签" aria-label="搜索 / 标签">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="7" />
          <path d="m21 21-4.3-4.3" />
        </svg>
      </a>
      <a class="icon-btn" :href="rssUrl" title="RSS" aria-label="RSS" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 11a9 9 0 0 1 9 9" />
          <path d="M4 4a16 16 0 0 1 16 16" />
          <circle cx="5" cy="19" r="1" fill="currentColor" stroke="none" />
        </svg>
      </a>
      <ThemeToggle />
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ThemeToggle from './ThemeToggle.vue'
import { link } from '../lib/site'

const props = defineProps<{ config: any }>()

const home = computed(() => link(''))
const tagUrl = computed(() => link('tag'))
const rssUrl = computed(() => link('rss.xml'))
</script>
