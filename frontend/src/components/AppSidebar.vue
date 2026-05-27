<script setup lang="ts">
import Icons from "./Icons.vue";

const lockedItems = [
  { label: "Historical Trends", icon: "trendingUp" },
  { label: "Asset Map", icon: "map" },
  { label: "Revenue Model", icon: "clock" },
  { label: "Admin Settings", icon: "settings" },
];
</script>

<template>
  <aside class="appSidebar">
    <nav class="flex h-full flex-col gap-2 p-4">
      <a
        class="navItem navItem--active"
        href="#"
        aria-current="page"
      >
        <Icons name="barChart" :size="18" />
        Market Performance
      </a>

      <div class="navSection">
        <button
          v-for="item in lockedItems"
          :key="item.label"
          class="lockedNavItem"
          disabled
          type="button"
        >
          <span class="flex items-center gap-3">
            <Icons :name="item.icon" :size="18" />
            {{ item.label }}
          </span>
          <Icons name="lock" :size="15" />
        </button>
      </div>
    </nav>
  </aside>
</template>
