<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import type { ProductPerformance, TimeSeriesPoint, UnitPerformance } from "../api";
import ChartSkeleton from "./ChartSkeleton.vue";

const DeliveryWindowChart = defineAsyncComponent(() => import("./charts/DeliveryWindowChart.vue"));
const ProductMixChart = defineAsyncComponent(() => import("./charts/ProductMixChart.vue"));
const UnitRevenueChart = defineAsyncComponent(() => import("./charts/UnitRevenueChart.vue"));

defineProps<{
  products: ProductPerformance[];
  timeseries: TimeSeriesPoint[];
  units: UnitPerformance[];
  loading: boolean;
}>();
</script>

<template>
  <section class="analysisDeck">
    <article class="workspaceSection">
      <div class="sectionHeader">
        <h2>Product Mix</h2>
      </div>
      <ChartSkeleton v-if="loading" />
      <ProductMixChart v-else :rows="products" />
    </article>
    <article class="workspaceSection">
      <div class="sectionHeader">
        <h2>Delivery Windows</h2>
      </div>
      <ChartSkeleton v-if="loading" />
      <DeliveryWindowChart v-else :rows="timeseries" />
    </article>
    <article class="workspaceSection">
      <div class="sectionHeader">
        <h2>Asset Revenue</h2>
      </div>
      <ChartSkeleton v-if="loading" />
      <UnitRevenueChart v-else :rows="units" />
    </article>
  </section>
</template>
