<script setup lang="ts">
import { computed } from "vue";
import type { Summary } from "../api";
import { currency } from "../utils/format";

const props = defineProps<{
  summary: Summary | null;
  loading: boolean;
}>();

const tickers = computed(() => [
  {
    label: "Accepted MW",
    value: (props.summary?.total_executed_quantity ?? 0).toFixed(0),
    detail: `${props.summary?.total_records ?? 0} results`,
  },
  {
    label: "Estimated gross value",
    value: currency(props.summary?.estimated_gross_revenue),
    detail: "availability estimate",
  },
  {
    label: "Avg price",
    value: `£${(props.summary?.average_clearing_price ?? 0).toFixed(2)}`,
    detail: "per MW/h",
  },
  {
    label: "Clearing assets",
    value: String(props.summary?.active_units ?? 0),
    detail: "units clearing",
  },
  {
    label: "Top service by MW",
    value: props.summary?.top_service_by_volume?.service_type ?? "-",
    detail: "by accepted MW",
  },
]);
</script>

<template>
  <section class="summaryTickerStrip" aria-label="Auction summary">
    <div v-for="ticker in tickers" :key="ticker.label" class="summaryTicker" :class="{ 'summaryTicker--loading': loading }">
      <span>{{ ticker.label }}</span>
      <strong>
        <template v-if="loading"><i></i></template>
        <template v-else>{{ ticker.value }}</template>
      </strong>
      <small>
        <template v-if="loading"><i></i></template>
        <template v-else>{{ ticker.detail }}</template>
      </small>
    </div>
  </section>
</template>
