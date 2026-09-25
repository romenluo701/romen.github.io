<template>
  <footer class="site-footer">
    <div>
      Copyright © {{ year }}
      <a :href="home">{{ config.title }}</a>
    </div>
    <div>
      Powered by
      <a href="https://meekdai.com/Gmeek.html" target="_blank" rel="noopener">Gmeek</a>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { link } from '../lib/site'

const props = defineProps<{ config: any }>()

const year = new Date().getFullYear()
const home = computed(() => link(''))
</script>
