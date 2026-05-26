<script setup lang="ts">
import { nextTick, onMounted, watch } from "vue";
import type { TimeSeriesPoint } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: TimeSeriesPoint[];
}>();

const { chartEl, setOption } = useEChart();

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
    tooltip: { trigger: "axis" },
    legend: { top: 0 },
    grid: { left: 48, right: 18, bottom: 32, top: 42 },
    xAxis: { type: "category", data: labels },
    yAxis: { type: "value", name: "MW" },
    series: services.map((service) => ({
      name: service,
      type: "bar",
      stack: "volume",
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
