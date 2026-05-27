<script setup lang="ts">
import { computed, nextTick, onMounted, watch } from "vue";
import type { ProductPerformance } from "../../api";
import type { AnalysisChartMode } from "../../chartModes";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: ProductPerformance[];
  mode: AnalysisChartMode;
}>();

const metricConfig = computed(() => {
  if (props.mode === "price") {
    return {
      axisName: "GBP/MW/h",
      color: "#E6E6E6",
      label: "Average clearing price",
      value: (row: ProductPerformance) => row.average_clearing_price,
    };
  }

  if (props.mode === "value") {
    return {
      axisName: "GBP",
      color: "#479FFA",
      label: "Estimated gross value",
      value: (row: ProductPerformance) => row.estimated_gross_revenue,
    };
  }

  return {
    axisName: "MW",
    color: "#4EBE96",
    label: "Accepted MW",
    value: (row: ProductPerformance) => row.executed_quantity,
  };
});

const topProducts = computed(() =>
  [...props.rows].sort((a, b) => metricConfig.value.value(b) - metricConfig.value.value(a)).slice(0, 8),
);
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
  () => [props.rows, props.mode],
  () => nextTick(render),
  { deep: true },
);

function render() {
  const metric = metricConfig.value;
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
    yAxis: { ...axisStyle, type: "value", name: metric.axisName },
    series: [
      {
        name: metric.label,
        type: "bar",
        data: topProducts.value.map((row) => metric.value(row)),
        itemStyle: { borderRadius: [4, 4, 0, 0], color: metric.color },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
