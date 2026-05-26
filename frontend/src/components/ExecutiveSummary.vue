<script setup lang="ts">
import type { Summary } from "../api";
import { currency } from "../utils/format";

defineProps<{
  summary: Summary | null;
  loading: boolean;
}>();
</script>

<template>
  <section class="metrics" aria-label="Executive summary">
    <template v-if="loading">
      <article v-for="index in 6" :key="index" class="animate-pulse">
        <span class="h-3 w-24 rounded bg-slate-100"></span>
        <strong class="h-8 w-28 rounded bg-slate-100"></strong>
      </article>
    </template>
    <article v-else>
      <span>Accepted MW</span>
      <strong>{{ (summary?.total_executed_quantity ?? 0).toFixed(0) }}</strong>
    </article>
    <article v-if="!loading">
      <span>Est. revenue</span>
      <strong>{{ currency(summary?.estimated_gross_revenue) }}</strong>
    </article>
    <article v-if="!loading">
      <span>Avg £/MW/h</span>
      <strong>{{ (summary?.average_clearing_price ?? 0).toFixed(2) }}</strong>
    </article>
    <article v-if="!loading">
      <span>Results</span>
      <strong>{{ summary?.total_records ?? 0 }}</strong>
    </article>
    <article v-if="!loading">
      <span>Active units</span>
      <strong>{{ summary?.active_units ?? 0 }}</strong>
    </article>
    <article v-if="!loading">
      <span>Top service</span>
      <strong>{{ summary?.top_service_by_volume?.service_type ?? "-" }}</strong>
    </article>
  </section>
</template>
