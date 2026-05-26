import type { EChartsOption } from "../lib/echarts";
import { onBeforeUnmount, onMounted, ref } from "vue";

type EChartsModule = typeof import("../lib/echarts");
type EChartsInstance = ReturnType<EChartsModule["init"]>;

let echartsModule: Promise<EChartsModule> | null = null;

export function useEChart() {
  const chartEl = ref<HTMLDivElement | null>(null);
  let chart: EChartsInstance | null = null;

  async function setOption(option: EChartsOption) {
    if (!chartEl.value) return;
    const echarts = await loadECharts();
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

function loadECharts() {
  echartsModule ??= import("../lib/echarts");
  return echartsModule;
}
