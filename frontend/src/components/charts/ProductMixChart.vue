<script setup lang="ts">
import { computed, nextTick, onMounted, watch } from "vue";
import type { ProductPerformance } from "../../api";
import { useEChart } from "../../composables/useEChart";

const props = defineProps<{
  rows: ProductPerformance[];
}>();

const topProducts = computed(() => props.rows.slice(0, 8));
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
    grid: { left: 52, right: 18, bottom: 72, top: 24 },
    xAxis: {
      type: "category",
      axisLabel: { rotate: 35 },
      data: topProducts.value.map((row) => `${row.service_type} ${row.auction_product}`),
    },
    yAxis: { type: "value", name: "MW" },
    series: [
      {
        name: "Accepted MW",
        type: "bar",
        data: topProducts.value.map((row) => row.executed_quantity),
        itemStyle: { color: "#2563eb" },
      },
    ],
  });
}
</script>

<template>
  <div ref="chartEl" class="chartBox compact"></div>
</template>
