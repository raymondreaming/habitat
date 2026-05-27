<script setup lang="ts">
import {
  Activity,
  BarChart3,
  CalendarDays,
  Check,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Clock3,
  CircleDollarSign,
  Lock,
  Map,
  Percent,
  RefreshCw,
  Search,
  Settings,
  ShieldAlert,
  Sparkles,
  TrendingUp,
  Zap,
} from "lucide-vue-next";

const icons = {
  activity: Activity,
  barChart: BarChart3,
  calendar: CalendarDays,
  check: Check,
  chevronDown: ChevronDown,
  chevronLeft: ChevronLeft,
  chevronRight: ChevronRight,
  clock: Clock3,
  dollar: CircleDollarSign,
  lock: Lock,
  map: Map,
  percent: Percent,
  refresh: RefreshCw,
  search: Search,
  settings: Settings,
  shield: ShieldAlert,
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
