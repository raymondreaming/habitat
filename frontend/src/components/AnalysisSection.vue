<script setup lang="ts">
import { computed, defineAsyncComponent, ref } from "vue";
import type { ProductPerformance, TimeSeriesPoint } from "../api";
import { ANALYSIS_CHART_MODES, type AnalysisChartMode } from "../chartModes";
import ChartModeSwitcher from "./ChartModeSwitcher.vue";
import ChartSkeleton from "./ChartSkeleton.vue";

const DeliveryWindowChart = defineAsyncComponent(() => import("./charts/DeliveryWindowChart.vue"));
const ProductMixChart = defineAsyncComponent(() => import("./charts/ProductMixChart.vue"));

defineProps<{
  products: ProductPerformance[];
  timeseries: TimeSeriesPoint[];
  loading: boolean;
}>();

const chartMode = ref<AnalysisChartMode>("volume");
const activeMode = computed(
  () => ANALYSIS_CHART_MODES.find((mode) => mode.id === chartMode.value) ?? ANALYSIS_CHART_MODES[0],
);

function updateChartMode(value: string) {
  if (value === "volume" || value === "price" || value === "value") {
    chartMode.value = value;
  }
}
</script>

<template>
  <section class="analysisLensSection">
    <div class="analysisLensHeader">
      <div>
        <h2>Analysis Lens</h2>
        <span>{{ activeMode.metricLabel }}</span>
      </div>
      <ChartModeSwitcher :model-value="chartMode" :modes="ANALYSIS_CHART_MODES" @update:model-value="updateChartMode" />
    </div>

    <div class="analysisDeck">
      <article class="workspaceSection">
        <div class="sectionHeader">
          <h2>Product Mix</h2>
        </div>
        <ChartSkeleton v-if="loading" />
        <ProductMixChart v-else :mode="chartMode" :rows="products" />
      </article>
      <article class="workspaceSection">
        <div class="sectionHeader">
          <h2>Delivery Windows</h2>
        </div>
        <ChartSkeleton v-if="loading" />
        <DeliveryWindowChart v-else :mode="chartMode" :rows="timeseries" />
      </article>
    </div>
  </section>
</template>
