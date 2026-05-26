<script setup lang="ts">
import { computed } from "vue";
import type { MarketShare, ProductPerformance, Summary, UnitPerformance } from "../api";
import { currency } from "../utils/format";

const props = defineProps<{
  summary: Summary | null;
  marketShare: MarketShare[];
  products: ProductPerformance[];
  units: UnitPerformance[];
  loading: boolean;
}>();

const strongestShare = computed(() =>
  props.marketShare
    .filter((row) => row.habitat_executed_quantity > 0)
    .sort((a, b) => b.habitat_market_share_percent - a.habitat_market_share_percent)[0],
);
const topProduct = computed(() => props.products[0]);
const topUnit = computed(() => props.units[0]);
</script>

<template>
  <section class="mb-5 grid gap-3 lg:grid-cols-3">
    <template v-if="loading">
      <article v-for="index in 3" :key="index" class="animate-pulse rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div class="h-3 w-32 rounded bg-slate-100"></div>
        <div class="mt-3 h-7 w-44 rounded bg-slate-100"></div>
      </article>
    </template>
    <article v-else class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <p class="text-xs font-extrabold uppercase text-slate-500">Best market position</p>
      <strong class="mt-2 block text-xl font-extrabold text-slate-950">
        {{ strongestShare ? `${strongestShare.service_type} ${strongestShare.habitat_market_share_percent.toFixed(1)}%` : "-" }}
      </strong>
    </article>
    <article v-if="!loading" class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <p class="text-xs font-extrabold uppercase text-slate-500">Top product</p>
      <strong class="mt-2 block text-xl font-extrabold text-slate-950">
        {{ topProduct ? `${topProduct.service_type} ${topProduct.auction_product}` : "-" }}
      </strong>
    </article>
    <article v-if="!loading" class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <p class="text-xs font-extrabold uppercase text-slate-500">Top unit value</p>
      <strong class="mt-2 block text-xl font-extrabold text-slate-950">
        {{ topUnit ? `${topUnit.auction_unit} ${currency(topUnit.estimated_gross_revenue)}` : currency(summary?.estimated_gross_revenue) }}
      </strong>
    </article>
  </section>
</template>
