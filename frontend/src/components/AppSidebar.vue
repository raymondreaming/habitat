<script setup lang="ts">
import Icons from "./Icons.vue";

const navItems = [
  { label: "Market Performance", icon: "barChart", active: true },
  { label: "Historical Trends", icon: "trendingUp" },
  { label: "Asset Map", icon: "map" },
  { label: "Revenue Model", icon: "clock" },
] as const;
</script>

<template>
  <aside class="appSidebar">
    <nav class="sidebarNav" aria-label="Primary">
      <a
        v-for="item in navItems"
        :key="item.label"
        class="navItem"
        :class="{ 'navItem--active': item.active }"
        href="#"
        :aria-current="item.active ? 'page' : undefined"
        :aria-label="item.label"
        :title="item.label"
      >
        <Icons :name="item.icon" :size="18" />
      </a>

      <button class="navItem navItem--bottom" type="button" aria-label="Admin Settings" title="Admin Settings">
        <Icons name="settings" :size="18" />
      </button>
    </nav>
  </aside>
</template>
