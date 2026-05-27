<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    points: number[];
    label?: string;
    width?: number;
    height?: number;
  }>(),
  {
    label: "trend",
    width: 92,
    height: 28,
  },
);

const path = computed(() => {
  if (props.points.length === 0) return "";

  const min = Math.min(...props.points);
  const max = Math.max(...props.points);
  const range = max - min || 1;
  const step = props.points.length > 1 ? props.width / (props.points.length - 1) : props.width;

  return props.points
    .map((point, index) => {
      const x = index * step;
      const y = props.height - ((point - min) / range) * props.height;
      return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(" ");
});

const tone = computed(() => {
  const first = props.points[0] ?? 0;
  const last = props.points.at(-1) ?? first;
  if (last > first) return "sparkline--up";
  if (last < first) return "sparkline--down";
  return "sparkline--flat";
});
</script>

<template>
  <svg class="sparkline" :class="tone" :viewBox="`0 0 ${width} ${height}`" role="img" :aria-label="label">
    <path class="sparkline__glow" :d="path" fill="none" />
    <path class="sparkline__line" :d="path" fill="none" />
  </svg>
</template>
