<script setup lang="ts">
import { RefreshCw } from "lucide-vue-next";
import { defineAsyncComponent } from "vue";
import type { MarketShare } from "../api";
import LoadingState from "./LoadingState.vue";

const MarketShareChart = defineAsyncComponent(() => import("./charts/MarketShareChart.vue"));

defineProps<{
  rows: MarketShare[];
  status: string;
  error: string;
  loading: boolean;
}>();

const emit = defineEmits<{
  refresh: [];
}>();
</script>

<template>
  <section class="panel">
    <div class="panelHeader">
      <div>
        <h2>Market Position</h2>
        <p v-if="status" class="status">{{ status }}</p>
      </div>
      <button class="secondary" type="button" @click="emit('refresh')">
        <RefreshCw :size="17" />
        Refresh
      </button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <LoadingState v-if="loading" label="Loading market position" />
    <div v-else class="marketGrid">
      <MarketShareChart :rows="rows" />
      <div class="shareTable">
        <table>
          <thead>
            <tr>
              <th>Service</th>
              <th>Habitat MW</th>
              <th>Market MW</th>
              <th>Share</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!rows.length">
              <td colspan="4">Update this day to load market comparison.</td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.service_type"
              v-memo="[row.habitat_executed_quantity, row.market_executed_quantity]"
            >
              <td>{{ row.service_type }}</td>
              <td>{{ row.habitat_executed_quantity.toFixed(0) }}</td>
              <td>{{ row.market_executed_quantity.toFixed(0) }}</td>
              <td>{{ row.habitat_market_share_percent.toFixed(1) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>
