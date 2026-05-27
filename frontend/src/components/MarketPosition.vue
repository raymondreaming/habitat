<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import type { MarketShare } from "../api";
import ChartSkeleton from "./ChartSkeleton.vue";
import Icons from "./Icons.vue";

const MarketShareChart = defineAsyncComponent(() => import("./charts/MarketShareChart.vue"));

const props = defineProps<{
  rows: MarketShare[];
  status: string;
  error: string;
  loading: boolean;
}>();

const emit = defineEmits<{
  refresh: [];
}>();

const strongestPosition = computed(() =>
  props.rows
    .filter((row) => row.habitat_executed_quantity > 0)
    .sort((a, b) => b.habitat_market_share_percent - a.habitat_market_share_percent)[0],
);

const interpretation = computed(() =>
  strongestPosition.value
    ? `Habitat's strongest position was ${strongestPosition.value.service_type}, clearing ${strongestPosition.value.habitat_market_share_percent.toFixed(1)}% of accepted market volume.`
    : "",
);
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
      <div class="shareTable">
        <p v-if="!loading && interpretation" class="marketInterpretation">{{ interpretation }}</p>
        <table>
          <thead>
            <tr>
              <th>Service</th>
              <th>Habitat MW</th>
              <th>Market MW</th>
              <th>Share</th>
              <th>Habitat £</th>
              <th>Market £</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="loading">
              <tr v-for="index in 5" :key="index" class="tableSkeletonRow">
                <td v-for="cell in 6" :key="cell"><span></span></td>
              </tr>
            </template>
            <tr v-else-if="!rows.length">
              <td colspan="6">Update this day to load market comparison.</td>
            </tr>
            <template v-else>
              <tr
                v-for="row in rows"
                :key="row.service_type"
                v-memo="[row.habitat_executed_quantity, row.market_executed_quantity]"
              >
                <td>{{ row.service_type }}</td>
                <td>{{ row.habitat_executed_quantity.toFixed(0) }}</td>
                <td>{{ row.market_executed_quantity.toFixed(0) }}</td>
                <td>{{ row.habitat_market_share_percent.toFixed(1) }}%</td>
                <td>{{ row.habitat_average_clearing_price.toFixed(2) }}</td>
                <td>{{ row.market_average_clearing_price.toFixed(2) }}</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>
