<script setup lang="ts">
import AnalysisSection from "./components/AnalysisSection.vue";
import AppHeader from "./components/AppHeader.vue";
import ExecutiveSummary from "./components/ExecutiveSummary.vue";
import MarketPosition from "./components/MarketPosition.vue";
import RawResultsPanel from "./components/RawResultsPanel.vue";
import { useDashboardData } from "./composables/useDashboardData";

const dashboard = useDashboardData();
</script>

<template>
  <main class="shell">
    <AppHeader
      :ingesting="dashboard.ingesting.value"
      :selected-date="dashboard.selectedDate.value"
      @ingest="dashboard.runIngest"
      @update:selected-date="dashboard.selectedDate.value = $event"
    />

    <ExecutiveSummary :summary="dashboard.summary.value" />

    <MarketPosition
      :error="dashboard.error.value"
      :rows="dashboard.marketShare.value"
      :status="dashboard.status.value"
      @refresh="dashboard.loadAll"
    />

    <AnalysisSection
      :products="dashboard.products.value"
      :timeseries="dashboard.timeseries.value"
      :units="dashboard.units.value"
    />

    <RawResultsPanel
      :auction-product="dashboard.auctionProduct.value"
      :auction-unit="dashboard.auctionUnit.value"
      :has-results="dashboard.hasResults.value"
      :loading="dashboard.loading.value"
      :options="dashboard.options.value"
      :results="dashboard.results.value"
      :service-type="dashboard.serviceType.value"
      @clear="dashboard.clearFilters"
      @update:auction-product="dashboard.auctionProduct.value = $event"
      @update:auction-unit="dashboard.auctionUnit.value = $event"
      @update:service-type="dashboard.serviceType.value = $event"
    />
  </main>
</template>
