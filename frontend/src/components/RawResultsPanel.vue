<script setup lang="ts">
import { useVirtualizer, type VirtualItem } from "@tanstack/vue-virtual";
import { computed, ref } from "vue";
import type { AuctionResult, Options } from "../api";
import Icons from "./Icons.vue";
import Sparkline from "./Sparkline.vue";

const props = defineProps<{
  results: AuctionResult[];
  options: Options | null;
  loading: boolean;
  hasResults: boolean;
  serviceType: string;
  auctionUnit: string;
  auctionProduct: string;
}>();

const emit = defineEmits<{
  "update:serviceType": [value: string];
  "update:auctionUnit": [value: string];
  "update:auctionProduct": [value: string];
  clear: [];
}>();

type VisibleResult = {
  item: VirtualItem;
  row: AuctionResult;
};

const virtualParent = ref<HTMLElement | null>(null);

const rowVirtualizer = useVirtualizer(
  computed(() => ({
    count: props.results.length,
    estimateSize: () => 58,
    getItemKey: (index) => props.results[index]?.unit_result_id ?? index,
    getScrollElement: () => virtualParent.value,
    overscan: 8,
  })),
);

const virtualRows = computed<VisibleResult[]>(() =>
  rowVirtualizer.value
    .getVirtualItems()
    .map((item) => ({ item, row: props.results[item.index] }))
    .filter((entry): entry is VisibleResult => Boolean(entry.row)),
);

const virtualHeight = computed(() => `${rowVirtualizer.value.getTotalSize()}px`);

const priceSeriesByResultId = computed(() => {
  const groups = new Map<string, AuctionResult[]>();
  const series = new Map<string, number[]>();

  for (const row of props.results) {
    const key = `${row.auction_unit}|${row.service_type}|${row.auction_product}`;
    groups.set(key, [...(groups.get(key) ?? []), row]);
  }

  for (const rows of groups.values()) {
    const values = [...rows].sort((a, b) => a.delivery_start.localeCompare(b.delivery_start));
    const points = values.map((row) => row.clearing_price);
    for (const row of values) series.set(row.unit_result_id, points);
  }

  return series;
});

function priceSeriesFor(row: AuctionResult) {
  return priceSeriesByResultId.value.get(row.unit_result_id) ?? [row.clearing_price];
}

function priceTrendLabel(row: AuctionResult) {
  const points = priceSeriesFor(row);
  const first = points[0] ?? row.clearing_price;
  const last = points.at(-1) ?? first;
  if (last > first) return "Rising price path";
  if (last < first) return "Falling price path";
  return "Flat price path";
}
</script>

<template>
  <section class="workspaceSection">
    <div class="sectionHeader sectionHeader--filters">
      <h2 class="headerWithIcon">
        <Icons name="activity" :size="17" />
        Auction Audit Trail
      </h2>
      <div class="filters">
        <label>
          <span>Service</span>
          <select :value="serviceType" @change="emit('update:serviceType', ($event.target as HTMLSelectElement).value)">
            <option value="">All</option>
            <option v-for="value in options?.service_types" :key="value" :value="value">{{ value }}</option>
          </select>
        </label>
        <label>
          <span>Unit</span>
          <select :value="auctionUnit" @change="emit('update:auctionUnit', ($event.target as HTMLSelectElement).value)">
            <option value="">All</option>
            <option v-for="value in options?.auction_units" :key="value" :value="value">{{ value }}</option>
          </select>
        </label>
        <label>
          <span>Product</span>
          <select :value="auctionProduct" @change="emit('update:auctionProduct', ($event.target as HTMLSelectElement).value)">
            <option value="">All</option>
            <option v-for="value in options?.auction_products" :key="value" :value="value">{{ value }}</option>
          </select>
        </label>
        <button class="secondary" type="button" @click="emit('clear')">
          <Icons name="search" :size="17" />
          Clear
        </button>
      </div>
    </div>

    <div class="tableWrap virtualResults">
      <div class="resultGrid virtualResults__header">
        <span>Delivery</span>
        <span>Unit</span>
        <span>Service</span>
        <span>Product</span>
        <span>MW</span>
        <span>£/MW/h</span>
        <span>Intraday price</span>
      </div>

      <div v-if="loading" class="virtualResults__loadingRows">
        <div v-for="index in 10" :key="index" class="resultGrid virtualResults__rowSkeleton">
          <span v-for="cell in 7" :key="cell"></span>
        </div>
      </div>

      <div v-else-if="!hasResults" class="virtualResults__state">No results for this selection.</div>

      <div v-else ref="virtualParent" class="virtualResults__body">
        <div class="virtualResults__spacer" :style="{ height: virtualHeight }">
          <div
            v-for="entry in virtualRows"
            :key="entry.row.unit_result_id"
            class="resultGrid virtualResults__row"
            :style="{ transform: `translateY(${entry.item.start}px)` }"
            v-memo="[entry.row.executed_quantity, entry.row.clearing_price, entry.row.delivery_start, entry.row.delivery_end]"
          >
            <span>{{ entry.row.delivery_start.slice(11, 16) }}-{{ entry.row.delivery_end.slice(11, 16) }}</span>
            <span>{{ entry.row.auction_unit }}</span>
            <span>{{ entry.row.service_type }}</span>
            <span>{{ entry.row.auction_product }}</span>
            <span>{{ entry.row.executed_quantity.toFixed(1) }}</span>
            <span>{{ entry.row.clearing_price.toFixed(2) }}</span>
            <span>
              <span class="resultTrend">
                <Sparkline :points="priceSeriesFor(entry.row)" :label="priceTrendLabel(entry.row)" />
                <span>{{ priceTrendLabel(entry.row).replace(" price path", "") }}</span>
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
