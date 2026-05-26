<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import type { ProductPerformance, TimeSeriesPoint, UnitPerformance } from "../api";
import TopUnitsLeaderboard from "./TopUnitsLeaderboard.vue";

const DeliveryWindowChart = defineAsyncComponent(() => import("./charts/DeliveryWindowChart.vue"));
const ProductMixChart = defineAsyncComponent(() => import("./charts/ProductMixChart.vue"));
const UnitRevenueChart = defineAsyncComponent(() => import("./charts/UnitRevenueChart.vue"));

defineProps<{
  products: ProductPerformance[];
  timeseries: TimeSeriesPoint[];
  units: UnitPerformance[];
}>();
</script>

<template>
  <section class="analysisGrid">
    <article class="panel">
      <h2>Product Mix</h2>
      <ProductMixChart :rows="products" />
    </article>
    <article class="panel">
      <h2>Delivery Windows</h2>
      <DeliveryWindowChart :rows="timeseries" />
    </article>
    <article class="panel">
      <h2>Unit Revenue</h2>
      <UnitRevenueChart :rows="units" />
    </article>
    <TopUnitsLeaderboard :units="units" />
  </section>
</template>
