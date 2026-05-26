<script setup lang="ts">
import { nextTick, onMounted, watch } from "vue";
import type { MarketShare } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: MarketShare[];
}>();

const { chartEl, setOption } = useEChart();

onMounted(render);
watch(
  () => props.rows,
  () => nextTick(render),
  { deep: true },
);

function render() {
  setOption({
    tooltip: { trigger: "axis" },
    legend: { top: 0 },
    grid: { left: 48, right: 18, bottom: 32, top: 42 },
    xAxis: { type: "category", data: props.rows.map((row) => row.service_type) },
    yAxis: { type: "value", name: "MW" },
    series: [
      {
        name: "Habitat",
        type: "bar",
        data: props.rows.map((row) => row.habitat_executed_quantity),
        itemStyle: { color: "#0f766e" },
      },
      {
        name: "Market",
        type: "bar",
        data: props.rows.map((row) => row.market_executed_quantity),
        itemStyle: { color: "#94a3b8" },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox"></div>
</template>
