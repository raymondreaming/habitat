<script setup lang="ts">
import { computed } from "vue";
import type { AuctionResult, MarketShare, ProductPerformance, Summary, UnitPerformance } from "../api";
import { currency } from "../utils/format";

const props = defineProps<{
  summary: Summary | null;
  marketShare: MarketShare[];
  products: ProductPerformance[];
  results: AuctionResult[];
  units: UnitPerformance[];
  loading: boolean;
}>();

const strongestShare = computed(() =>
  props.marketShare
    .filter((row) => row.habitat_executed_quantity > 0)
    .sort((a, b) => b.habitat_market_share_percent - a.habitat_market_share_percent)[0],
);
const topProduct = computed(() => [...props.products].sort((a, b) => b.estimated_gross_revenue - a.estimated_gross_revenue)[0]);
const topUnit = computed(() => [...props.units].sort((a, b) => b.estimated_gross_revenue - a.estimated_gross_revenue)[0]);
const bestPricePremium = computed(() =>
  props.marketShare
    .filter((row) => row.habitat_records > 0 && row.market_records > 0)
    .map((row) => ({
      premium: row.habitat_average_clearing_price - row.market_average_clearing_price,
      serviceType: row.service_type,
    }))
    .sort((a, b) => b.premium - a.premium)[0],
);
const negativePriceExposure = computed(() => {
  const rows = props.results.filter((row) => row.clearing_price < 0);
  return {
    count: rows.length,
    volume: rows.reduce((sum, row) => sum + row.executed_quantity, 0),
  };
});
const signals = computed(() => [
  {
    label: "Strongest market position",
    value: strongestShare.value
      ? `${strongestShare.value.service_type} ${strongestShare.value.habitat_market_share_percent.toFixed(1)}%`
      : "-",
    detail: "of accepted market MW",
  },
  {
    label: "Highest-value product",
    value: topProduct.value ? currency(topProduct.value.estimated_gross_revenue) : "-",
    detail: topProduct.value ? `${topProduct.value.service_type} ${topProduct.value.auction_product}` : "no product data",
  },
  {
    label: "Top contributing asset",
    value: topUnit.value ? topUnit.value.auction_unit : "-",
    detail: topUnit.value ? currency(topUnit.value.estimated_gross_revenue) : "no unit data",
  },
  {
    label: "Best price premium",
    value: bestPricePremium.value ? `£${bestPricePremium.value.premium.toFixed(2)}` : "-",
    detail: bestPricePremium.value ? `${bestPricePremium.value.serviceType} vs market avg` : "no market comparison",
  },
  {
    label: "Negative-price exposure",
    value: negativePriceExposure.value.count > 0 ? `${negativePriceExposure.value.volume.toFixed(0)} MW` : "None",
    detail:
      negativePriceExposure.value.count > 0
        ? `${negativePriceExposure.value.count} accepted rows below £0`
        : "no accepted rows below £0",
  },
]);
</script>

<template>
  <section class="insightRail">
    <div class="insightRail__items">
      <article v-for="signal in signals" :key="signal.label" class="insightCell" :class="{ 'insightCell--loading': loading }">
        <p>{{ signal.label }}</p>
        <strong>
          <template v-if="loading"><i></i></template>
          <template v-else>{{ signal.value }}</template>
        </strong>
        <span>
          <template v-if="loading"><i></i></template>
          <template v-else>{{ signal.detail }}</template>
        </span>
      </article>
    </div>
  </section>
</template>
