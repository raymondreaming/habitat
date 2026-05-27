<script setup lang="ts">
import type { MarketShare } from "../api";

defineProps<{
  rows: MarketShare[];
  loading: boolean;
}>();
</script>

<template>
  <section class="workspaceSection marketComparisonSection">
    <div class="sectionHeader">
      <div>
        <h2>Market Comparison</h2>
        <p>Habitat accepted volume and average clearing price against the wider market.</p>
      </div>
    </div>

    <div class="shareTable shareTable--full">
      <table>
        <thead>
          <tr>
            <th>Service</th>
            <th>Habitat MW</th>
            <th>Market MW</th>
            <th>Share</th>
            <th>Habitat £</th>
            <th>Market £</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr v-for="index in 5" :key="index" class="tableSkeletonRow">
              <td v-for="cell in 6" :key="cell"><span></span></td>
            </tr>
          </template>
          <tr v-else-if="!rows.length">
            <td colspan="6">Update this day to load market comparison.</td>
          </tr>
          <template v-else>
            <tr
              v-for="row in rows"
              :key="row.service_type"
              v-memo="[row.habitat_executed_quantity, row.market_executed_quantity]"
            >
              <td>{{ row.service_type }}</td>
              <td>{{ row.habitat_executed_quantity.toFixed(0) }}</td>
              <td>{{ row.market_executed_quantity.toFixed(0) }}</td>
              <td>{{ row.habitat_market_share_percent.toFixed(1) }}%</td>
              <td>{{ row.habitat_average_clearing_price.toFixed(2) }}</td>
              <td>{{ row.market_average_clearing_price.toFixed(2) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </section>
</template>
