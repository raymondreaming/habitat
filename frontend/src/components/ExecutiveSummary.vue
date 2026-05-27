<script setup lang="ts">
import { computed } from "vue";
import type { Summary } from "../api";
import { currency } from "../utils/format";

const props = defineProps<{
  summary: Summary | null;
  loading: boolean;
}>();

const metrics = computed(() => [
  {
    label: "Accepted volume",
    value: (props.summary?.total_executed_quantity ?? 0).toFixed(0),
    detail: "MW cleared",
  },
  {
    label: "Estimated value",
    value: currency(props.summary?.estimated_gross_revenue),
    detail: "gross availability",
  },
  {
    label: "Average price",
    value: `£${(props.summary?.average_clearing_price ?? 0).toFixed(2)}`,
    detail: "per MW/h",
  },
  {
    label: "Accepted results",
    value: String(props.summary?.total_records ?? 0),
    detail: "market rows",
  },
  {
    label: "Active assets",
    value: String(props.summary?.active_units ?? 0),
    detail: "units clearing",
  },
  {
    label: "Leading service",
    value: props.summary?.top_service_by_volume?.service_type ?? "-",
    detail: "by accepted MW",
  },
]);
</script>

<template>
  <section class="summaryBoard" aria-label="Executive summary">
    <template v-if="loading">
      <div class="summaryBoard__primary animate-pulse">
        <div class="h-3 w-32 rounded bg-white/10"></div>
        <div class="mt-8 h-16 w-56 rounded bg-white/10"></div>
        <div class="mt-5 h-4 w-44 rounded bg-white/10"></div>
      </div>
      <div class="summaryBoard__grid">
        <article v-for="index in 5" :key="index" class="summaryMetric animate-pulse">
          <div class="h-3 w-24 rounded bg-white/10"></div>
          <div class="mt-5 h-8 w-28 rounded bg-white/10"></div>
          <div class="mt-3 h-3 w-20 rounded bg-white/10"></div>
        </article>
      </div>
    </template>

    <template v-else>
      <div class="summaryBoard__primary">
        <p>{{ metrics[0].label }}</p>
        <strong>{{ metrics[0].value }}</strong>
        <span>{{ metrics[0].detail }} across {{ metrics[3].value }} accepted results</span>
      </div>

      <div class="summaryBoard__grid">
        <article v-for="metric in metrics.slice(1)" :key="metric.label" class="summaryMetric">
          <p>{{ metric.label }}</p>
          <strong>{{ metric.value }}</strong>
          <span>{{ metric.detail }}</span>
        </article>
      </div>
    </template>
  </section>
</template>
