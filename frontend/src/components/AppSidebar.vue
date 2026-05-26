<script setup lang="ts">
import { BarChart3, Clock3, Lock, Map, Settings, TrendingUp } from "lucide-vue-next";

const lockedItems = [
  { label: "Historical Trends", icon: TrendingUp },
  { label: "Asset Map", icon: Map },
  { label: "Revenue Model", icon: Clock3 },
  { label: "Admin Settings", icon: Settings },
];
</script>

<template>
  <aside class="fixed bottom-0 left-0 top-16 z-30 hidden w-64 overflow-y-auto border-r border-slate-200 bg-white lg:block">
    <nav class="flex h-full flex-col gap-2 p-4">
      <a
        class="flex items-center gap-3 rounded-md bg-slate-900 px-3 py-2.5 text-sm font-bold text-white"
        href="#"
        aria-current="page"
      >
        <BarChart3 :size="18" />
        Market Performance
      </a>

      <div class="mt-3 border-t border-slate-200 pt-3">
        <p class="px-3 pb-2 text-xs font-bold uppercase text-slate-500">Locked</p>
        <button
          v-for="item in lockedItems"
          :key="item.label"
          class="mt-1 flex w-full cursor-not-allowed items-center justify-between rounded-md bg-transparent px-3 py-2.5 text-left text-sm font-semibold text-slate-400"
          disabled
          type="button"
        >
          <span class="flex items-center gap-3">
            <component :is="item.icon" :size="18" />
            {{ item.label }}
          </span>
          <Lock :size="15" />
        </button>
      </div>
    </nav>
  </aside>
</template>
