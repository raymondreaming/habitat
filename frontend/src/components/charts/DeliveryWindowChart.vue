<script setup lang="ts">
import { computed, nextTick, onMounted, watch } from "vue";
import type { TimeSeriesPoint } from "../../api";
import type { AnalysisChartMode } from "../../chartModes";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: TimeSeriesPoint[];
  mode: AnalysisChartMode;
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

const metricConfig = computed(() => {
  if (props.mode === "price") {
    return {
      axisName: "GBP/MW/h",
      stack: undefined,
      seriesName: "Average price",
      value: (rows: TimeSeriesPoint[]) => {
        const totalVolume = rows.reduce((sum, row) => sum + row.executed_quantity, 0);
        if (totalVolume === 0) return 0;
        return rows.reduce((sum, row) => sum + row.average_clearing_price * row.executed_quantity, 0) / totalVolume;
      },
    };
  }

  if (props.mode === "value") {
    return {
      axisName: "GBP",
      stack: "value",
      seriesName: "Estimated value",
      value: (rows: TimeSeriesPoint[]) => rows.reduce((sum, row) => sum + row.estimated_gross_revenue, 0),
    };
  }

  return {
    axisName: "MW",
    stack: "volume",
    seriesName: "Accepted MW",
    value: (rows: TimeSeriesPoint[]) => rows.reduce((sum, row) => sum + row.executed_quantity, 0),
  };
});

onMounted(render);
watch(
  () => [props.rows, props.mode],
  () => nextTick(render),
  { deep: true },
);

function render() {
  const metric = metricConfig.value;
  const labels = Array.from(new Set(props.rows.map((row) => row.delivery_start.slice(11, 16))));
  const services = Array.from(new Set(props.rows.map((row) => row.service_type)));
  setOption({
    color: ["#479FFA", "#868F97", "#E6E6E6", "#404044"],
    textStyle: { color: "#E6E6E6" },
    tooltip: { ...tooltipStyle, trigger: "axis" },
    legend: { top: 0, textStyle: { color: "#E6E6E6" } },
    grid: { left: 48, right: 18, bottom: 32, top: 42 },
    xAxis: { ...axisStyle, type: "category", data: labels },
    yAxis: { ...axisStyle, type: "value", name: metric.axisName },
    series: services.map((service) => ({
      name: service,
      type: "bar",
      stack: metric.stack,
      itemStyle: { borderRadius: [3, 3, 0, 0] },
      emphasis: { focus: "series" },
      data: labels.map((label) => {
        const rows = props.rows.filter((row) => row.delivery_start.slice(11, 16) === label && row.service_type === service);
        return metric.value(rows);
      }),
    })),
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
