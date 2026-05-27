<script setup lang="ts">
import { computed, nextTick, onMounted, watch } from "vue";
import type { UnitPerformance } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: UnitPerformance[];
}>();

const topUnits = computed(() => props.rows.slice(0, 8));
const { chartEl, setOption } = useEChart();
const axisStyle = {
  axisLabel: { color: "#868F97" },
  axisLine: { lineStyle: { color: "rgba(255, 255, 255, 0.1)" } },
  splitLine: { lineStyle: { color: "rgba(255, 255, 255, 0.06)" } },
};
const tooltipStyle = {
  backgroundColor: "rgba(0, 0, 0, 0.85)",
  borderColor: "rgba(255, 255, 255, 0.1)",
  textStyle: { color: "#FFFFFF" },
};

onMounted(render);
watch(
  () => props.rows,
  () => nextTick(render),
  { deep: true },
);

function render() {
  const rows = [...topUnits.value].reverse();
  setOption({
    textStyle: { color: "#E6E6E6" },
    tooltip: { ...tooltipStyle, trigger: "axis" },
    grid: { left: 96, right: 18, bottom: 28, top: 20 },
    xAxis: { ...axisStyle, type: "value", name: "GBP" },
    yAxis: { ...axisStyle, type: "category", data: rows.map((row) => row.auction_unit) },
    series: [
      {
        name: "Estimated revenue",
        type: "bar",
        data: rows.map((row) => row.estimated_gross_revenue),
        itemStyle: { borderRadius: [0, 4, 4, 0], color: "#E6E6E6" },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
