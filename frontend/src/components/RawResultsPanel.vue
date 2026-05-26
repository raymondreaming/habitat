<script setup lang="ts">
import { Search } from "lucide-vue-next";
import type { AuctionResult, Options } from "../api";

defineProps<{
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
</script>

<template>
  <section class="panel">
    <div class="panelHeader">
      <h2>Raw Results</h2>
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
          <Search :size="17" />
          Clear
        </button>
      </div>
    </div>

    <div class="tableWrap">
      <table>
        <thead>
          <tr>
            <th>Delivery</th>
            <th>Unit</th>
            <th>Service</th>
            <th>Product</th>
            <th>MW</th>
            <th>£/MW/h</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6">Loading...</td>
          </tr>
          <tr v-else-if="!hasResults">
            <td colspan="6">No stored results for this selection.</td>
          </tr>
          <tr
            v-for="row in results"
            v-else
            :key="row.unit_result_id"
            v-memo="[row.executed_quantity, row.clearing_price, row.delivery_start, row.delivery_end]"
          >
            <td>{{ row.delivery_start.slice(11, 16) }}-{{ row.delivery_end.slice(11, 16) }}</td>
            <td>{{ row.auction_unit }}</td>
            <td>{{ row.service_type }}</td>
            <td>{{ row.auction_product }}</td>
            <td>{{ row.executed_quantity.toFixed(1) }}</td>
            <td>{{ row.clearing_price.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
