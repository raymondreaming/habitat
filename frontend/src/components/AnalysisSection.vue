<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import type { ProductPerformance, TimeSeriesPoint, UnitPerformance } from "../api";
import LoadingState from "./LoadingState.vue";
import TopUnitsLeaderboard from "./TopUnitsLeaderboard.vue";

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
  <section class="analysisGrid">
    <article class="panel">
      <h2>Product Mix</h2>
      <LoadingState v-if="loading" label="Loading product mix" />
      <ProductMixChart v-else :rows="products" />
    </article>
    <article class="panel">
      <h2>Delivery Windows</h2>
      <LoadingState v-if="loading" label="Loading delivery windows" />
      <DeliveryWindowChart v-else :rows="timeseries" />
    </article>
    <article class="panel">
      <h2>Asset Revenue</h2>
      <LoadingState v-if="loading" label="Loading asset revenue" />
      <UnitRevenueChart v-else :rows="units" />
    </article>
    <LoadingState v-if="loading" label="Loading top units" />
    <TopUnitsLeaderboard v-else :units="units" />
  </section>
</template>
