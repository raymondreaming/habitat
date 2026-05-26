<script setup lang="ts">
import type { ProductPerformance, TimeSeriesPoint, UnitPerformance } from "../api";
import DeliveryWindowChart from "./charts/DeliveryWindowChart.vue";
import ProductMixChart from "./charts/ProductMixChart.vue";
import UnitRevenueChart from "./charts/UnitRevenueChart.vue";
import TopUnitsLeaderboard from "./TopUnitsLeaderboard.vue";

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
