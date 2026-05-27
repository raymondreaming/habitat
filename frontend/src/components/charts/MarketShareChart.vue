<script setup lang="ts">
import { nextTick, onMounted, watch } from "vue";
import type { MarketShare } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: MarketShare[];
}>();

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
  setOption({
    color: ["#479FFA", "#868F97"],
    textStyle: { color: "#E6E6E6" },
    tooltip: { ...tooltipStyle, trigger: "axis" },
    legend: { top: 0, textStyle: { color: "#E6E6E6" } },
    grid: { left: 48, right: 18, bottom: 32, top: 42 },
    xAxis: { ...axisStyle, type: "category", data: props.rows.map((row) => row.service_type) },
    yAxis: { ...axisStyle, type: "value", name: "MW" },
    series: [
      {
        name: "Habitat",
        type: "bar",
        data: props.rows.map((row) => row.habitat_executed_quantity),
        itemStyle: { borderRadius: [4, 4, 0, 0], color: "#479FFA" },
      },
      {
        name: "Market",
        type: "bar",
        data: props.rows.map((row) => row.market_executed_quantity),
        itemStyle: { borderRadius: [4, 4, 0, 0], color: "rgba(134, 143, 151, 0.46)" },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox"></div>
</template>
