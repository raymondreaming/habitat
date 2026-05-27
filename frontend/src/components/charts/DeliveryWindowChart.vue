<script setup lang="ts">
import { nextTick, onMounted, watch } from "vue";
import type { TimeSeriesPoint } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: TimeSeriesPoint[];
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
  const labels = Array.from(new Set(props.rows.map((row) => row.delivery_start.slice(11, 16))));
  const services = Array.from(new Set(props.rows.map((row) => row.service_type)));
  setOption({
    color: ["#479FFA", "#868F97", "#E6E6E6", "#404044"],
    textStyle: { color: "#E6E6E6" },
    tooltip: { ...tooltipStyle, trigger: "axis" },
    legend: { top: 0, textStyle: { color: "#E6E6E6" } },
    grid: { left: 48, right: 18, bottom: 32, top: 42 },
    xAxis: { ...axisStyle, type: "category", data: labels },
    yAxis: { ...axisStyle, type: "value", name: "MW" },
    series: services.map((service) => ({
      name: service,
      type: "bar",
      stack: "volume",
      itemStyle: { borderRadius: [3, 3, 0, 0] },
      data: labels.map((label) =>
        props.rows
          .filter((row) => row.delivery_start.slice(11, 16) === label && row.service_type === service)
          .reduce((sum, row) => sum + row.executed_quantity, 0),
      ),
    })),
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
