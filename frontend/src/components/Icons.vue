<script setup lang="ts">
import {
  Activity,
  BarChart3,
  CalendarDays,
  Clock3,
  Lock,
  Map,
  RefreshCw,
  Search,
  Settings,
  Sparkles,
  TrendingUp,
  Zap,
} from "lucide-vue-next";

const icons = {
  activity: Activity,
  barChart: BarChart3,
  calendar: CalendarDays,
  clock: Clock3,
  lock: Lock,
  map: Map,
  refresh: RefreshCw,
  search: Search,
  settings: Settings,
  sparkles: Sparkles,
  trendingUp: TrendingUp,
  zap: Zap,
} as const;

defineOptions({
  inheritAttrs: false,
});

defineProps<{
  name: keyof typeof icons;
  size?: number;
  strokeWidth?: number;
}>();
</script>

<template>
  <component :is="icons[name]" v-bind="$attrs" :size="size ?? 17" :stroke-width="strokeWidth ?? 2" aria-hidden="true" />
</template>
