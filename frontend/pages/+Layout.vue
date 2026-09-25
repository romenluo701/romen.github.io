<template>
  <SiteHeader :config="config" />
  <main class="site-content">
    <slot />
  </main>
  <SiteFooter :config="config" />
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useData } from 'vike-vue/useData'
import SiteHeader from '../components/SiteHeader.vue'
import SiteFooter from '../components/SiteFooter.vue'
import { useTheme } from '../composables/useTheme'
import '../styles/tokens.css'
import '../styles/global.css'

const data = useData() as any
const config = computed(() => data?.config ?? { title: '博客', subTitle: '', avatarUrl: '' })

const { sync } = useTheme()
onMounted(sync)
</script>
