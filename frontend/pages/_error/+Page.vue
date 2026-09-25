<template>
  <div class="notfound">
    <h1>404</h1>
    <p>页面不存在或已被移除</p>
    <p><a :href="home">返回首页</a></p>
  </div>
</template>

<script setup lang="ts">
import { link } from '../../lib/site'

const home = link('')
</script>
