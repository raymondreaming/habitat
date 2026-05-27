<script setup lang="ts">
import { computed, nextTick, onMounted, watch } from "vue";
import type { ProductPerformance } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: ProductPerformance[];
}>();

const topProducts = computed(() => props.rows.slice(0, 8));
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
    textStyle: { color: "#E6E6E6" },
    tooltip: { ...tooltipStyle, trigger: "axis" },
    grid: { left: 52, right: 18, bottom: 72, top: 24 },
    xAxis: {
      ...axisStyle,
      type: "category",
      axisLabel: { color: "#868F97", rotate: 35 },
      data: topProducts.value.map((row) => `${row.service_type} ${row.auction_product}`),
    },
    yAxis: { ...axisStyle, type: "value", name: "GBP" },
    series: [
      {
        name: "Estimated gross value",
        type: "bar",
        data: topProducts.value.map((row) => row.estimated_gross_revenue),
        itemStyle: { borderRadius: [4, 4, 0, 0], color: "#479FFA" },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
