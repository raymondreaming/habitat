<script setup lang="ts">
import type { Summary } from "../api";
import { currency } from "../utils/format";

defineProps<{
  summary: Summary | null;
}>();
</script>

<template>
  <section class="metrics" aria-label="Executive summary">
    <article>
      <span>Accepted MW</span>
      <strong>{{ (summary?.total_executed_quantity ?? 0).toFixed(0) }}</strong>
    </article>
    <article>
      <span>Est. revenue</span>
      <strong>{{ currency(summary?.estimated_gross_revenue) }}</strong>
    </article>
    <article>
      <span>Avg £/MW/h</span>
      <strong>{{ (summary?.average_clearing_price ?? 0).toFixed(2) }}</strong>
    </article>
    <article>
      <span>Results</span>
      <strong>{{ summary?.total_records ?? 0 }}</strong>
    </article>
    <article>
      <span>Active units</span>
      <strong>{{ summary?.active_units ?? 0 }}</strong>
    </article>
    <article>
      <span>Top service</span>
      <strong>{{ summary?.top_service_by_volume?.service_type ?? "-" }}</strong>
    </article>
  </section>
</template>
