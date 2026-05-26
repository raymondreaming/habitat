<script setup lang="ts">
import { computed, nextTick, onMounted, watch } from "vue";
import type { UnitPerformance } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: UnitPerformance[];
}>();

const topUnits = computed(() => props.rows.slice(0, 8));
const { chartEl, setOption } = useEChart();

onMounted(render);
watch(
  () => props.rows,
  () => nextTick(render),
  { deep: true },
);

function render() {
  const rows = [...topUnits.value].reverse();
  setOption({
    tooltip: { trigger: "axis" },
    grid: { left: 96, right: 18, bottom: 28, top: 20 },
    xAxis: { type: "value", name: "GBP" },
    yAxis: { type: "category", data: rows.map((row) => row.auction_unit) },
    series: [
      {
        name: "Estimated revenue",
        type: "bar",
        data: rows.map((row) => row.estimated_gross_revenue),
        itemStyle: { color: "#9333ea" },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
