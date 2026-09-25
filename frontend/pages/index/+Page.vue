<template>
  <div>
    <p v-if="config.subTitle" class="site-subtitle">{{ config.subTitle }}</p>
    <ul class="post-list">
      <PostCard
        v-for="post in posts"
        :key="post.slug"
        :post="post"
        :label-color-dict="labelColorDict"
      />
    </ul>
    <div v-if="posts.length === 0" class="empty-tip">暂无文章</div>
  </div>
</template>

<script setup lang="ts">
import { useData } from 'vike-vue/useData'
import PostCard from '../../components/PostCard.vue'

const data = useData() as any
const config = data.config
const posts = data.postList.posts
const labelColorDict = data.postList.labelColorDict
</script>
