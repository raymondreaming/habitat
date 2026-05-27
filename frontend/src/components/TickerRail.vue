<script setup lang="ts">
import { computed } from "vue";
import type { MarketShare, ProductPerformance, Summary, UnitPerformance } from "../api";
import { currency } from "../utils/format";
import Icons from "./Icons.vue";

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
const topUnits = computed(() => [...props.units].sort((a, b) => b.estimated_gross_revenue - a.estimated_gross_revenue).slice(0, 5));

const tickers = computed(() => [
  {
    label: "Best share",
    value: strongestShare.value ? `${strongestShare.value.habitat_market_share_percent.toFixed(1)}%` : "-",
    detail: strongestShare.value?.service_type ?? "no market share",
  },
  {
    label: "Top product",
    value: topProduct.value ? `${topProduct.value.executed_quantity.toFixed(0)} MW` : "-",
    detail: topProduct.value ? `${topProduct.value.service_type} ${topProduct.value.auction_product}` : "no product data",
  },
  {
    label: "Top unit",
    value: topUnit.value ? `${topUnit.value.executed_quantity.toFixed(0)} MW` : "-",
    detail: topUnit.value?.auction_unit ?? "no unit data",
  },
  {
    label: "Leading service",
    value: props.summary?.top_service_by_volume?.service_type ?? "-",
    detail: props.summary?.top_service_by_volume
      ? `${props.summary.top_service_by_volume.executed_quantity.toFixed(0)} MW`
      : "no service data",
  },
  {
    label: "Active assets",
    value: String(props.summary?.active_units ?? 0),
    detail: `${props.summary?.total_records ?? 0} accepted rows`,
  },
]);
</script>

<template>
  <aside class="tickerRail">
    <div class="tickerRail__header">
      <Icons name="activity" :size="16" />
      <span>Market Tape</span>
    </div>

    <div class="tickerRail__list">
      <template v-if="loading">
        <div v-for="index in 6" :key="index" class="tickerItem tickerItem--loading">
          <span></span>
          <strong></strong>
          <small></small>
        </div>
      </template>

      <template v-else>
        <div v-for="ticker in tickers" :key="ticker.label" class="tickerItem">
          <span>{{ ticker.label }}</span>
          <strong>{{ ticker.value }}</strong>
          <small>{{ ticker.detail }}</small>
        </div>
      </template>
    </div>

    <div class="tickerRail__units">
      <div class="tickerRail__header">
        <Icons name="zap" :size="16" />
        <span>Top Units</span>
      </div>
      <ol>
        <template v-if="loading">
          <li v-for="index in 5" :key="index" class="railUnit railUnit--loading">
            <span>{{ String(index).padStart(2, "0") }}</span>
            <strong><i></i></strong>
            <small><i></i></small>
          </li>
        </template>
        <template v-else>
          <li v-for="(unit, index) in topUnits" :key="unit.auction_unit" class="railUnit">
            <span>{{ String(index + 1).padStart(2, "0") }}</span>
            <strong>{{ unit.auction_unit }}</strong>
            <small>{{ currency(unit.estimated_gross_revenue) }} · {{ unit.executed_quantity.toFixed(0) }} MW</small>
          </li>
        </template>
      </ol>
    </div>
  </aside>
</template>
