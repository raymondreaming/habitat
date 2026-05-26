import * as echarts from "echarts";
import type { EChartsOption } from "echarts";
import { onBeforeUnmount, onMounted, ref } from "vue";

export function useEChart() {
  const chartEl = ref<HTMLDivElement | null>(null);
  let chart: echarts.ECharts | null = null;

  function setOption(option: EChartsOption) {
    if (!chartEl.value) return;
    chart ??= echarts.init(chartEl.value);
    chart.setOption(option, true);
  }

  function resize() {
    chart?.resize();
  }

  onMounted(() => {
    window.addEventListener("resize", resize);
  });

  onBeforeUnmount(() => {
    window.removeEventListener("resize", resize);
    chart?.dispose();
  });

  return {
    chartEl,
    setOption,
    resize,
  };
}
