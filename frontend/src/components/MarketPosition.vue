<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import type { MarketShare, UnitPerformance } from "../api";
import ChartSkeleton from "./ChartSkeleton.vue";
import Icons from "./Icons.vue";

const MarketShareChart = defineAsyncComponent(() => import("./charts/MarketShareChart.vue"));
const UnitRevenueChart = defineAsyncComponent(() => import("./charts/UnitRevenueChart.vue"));

defineProps<{
  rows: MarketShare[];
  units: UnitPerformance[];
  status: string;
  error: string;
  loading: boolean;
}>();

const emit = defineEmits<{
  refresh: [];
}>();

</script>

<template>
  <section class="workspaceSection workspaceSection--market">
    <div class="sectionHeader">
      <div>
        <h2>Market Position</h2>
        <p v-if="status" class="status">{{ status }}</p>
      </div>
      <button class="secondary" type="button" @click="emit('refresh')">
        <Icons name="refresh" :size="17" />
        Refresh
      </button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="marketGrid">
      <ChartSkeleton v-if="loading" />
      <MarketShareChart v-else :rows="rows" />

      <div class="marketSideStack">
        <div class="marketSidePanel">
          <div class="sectionHeader sectionHeader--compact">
            <h2>Asset Revenue</h2>
          </div>
          <ChartSkeleton v-if="loading" />
          <UnitRevenueChart v-else :rows="units" />
        </div>
      </div>
    </div>
  </section>
</template>
