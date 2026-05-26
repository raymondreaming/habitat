<script setup lang="ts">
import AnalysisSection from "./components/AnalysisSection.vue";
import AppHeader from "./components/AppHeader.vue";
import AppSidebar from "./components/AppSidebar.vue";
import ExecutiveSummary from "./components/ExecutiveSummary.vue";
import InsightStrip from "./components/InsightStrip.vue";
import MarketPosition from "./components/MarketPosition.vue";
import NoDataPanel from "./components/NoDataPanel.vue";
import PageToolbar from "./components/PageToolbar.vue";
import RawResultsPanel from "./components/RawResultsPanel.vue";
import { useDashboardData } from "./composables/useDashboardData";

const dashboard = useDashboardData();
</script>

<template>
  <main class="min-h-screen bg-[#f5f7f6]">
    <AppHeader />

    <div class="min-h-[calc(100vh-4rem)]">
      <AppSidebar />

      <div class="min-w-0 lg:pl-64">
        <div class="shell">
          <PageToolbar
            :has-stored-data="dashboard.hasStoredDataForDate.value"
            :ingesting="dashboard.ingesting.value"
            :loading="dashboard.loading.value"
            :latest-date="dashboard.latestStoredDate.value"
            :selected-date="dashboard.selectedDate.value"
            :status="dashboard.status.value"
            @ingest="dashboard.runIngest"
            @select-latest="dashboard.selectLatestDate"
            @update:selected-date="dashboard.selectedDate.value = $event"
          />

          <ExecutiveSummary :loading="dashboard.loading.value" :summary="dashboard.summary.value" />

          <NoDataPanel
            v-if="!dashboard.loading.value && !dashboard.error.value && !dashboard.hasStoredDataForDate.value"
            :ingesting="dashboard.ingesting.value"
            :latest-date="dashboard.latestStoredDate.value"
            :selected-date="dashboard.selectedDate.value"
            @ingest="dashboard.runIngest"
            @select-latest="dashboard.selectLatestDate"
          />

          <InsightStrip
            :loading="dashboard.loading.value"
            :market-share="dashboard.marketShare.value"
            :products="dashboard.products.value"
            :summary="dashboard.summary.value"
            :units="dashboard.units.value"
          />

          <MarketPosition
            :error="dashboard.error.value"
            :loading="dashboard.loading.value"
            :rows="dashboard.marketShare.value"
            :status="dashboard.status.value"
            @refresh="dashboard.loadAll"
          />

          <AnalysisSection
            :loading="dashboard.loading.value"
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
        </div>
      </div>
    </div>
  </main>
</template>
