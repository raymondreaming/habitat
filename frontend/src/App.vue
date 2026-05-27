<script setup lang="ts">
import AnalysisSection from "./components/AnalysisSection.vue";
import AppHeader from "./components/AppHeader.vue";
import AppSidebar from "./components/AppSidebar.vue";
import InsightStrip from "./components/InsightStrip.vue";
import MarketComparisonTable from "./components/MarketComparisonTable.vue";
import MarketPosition from "./components/MarketPosition.vue";
import NoDataPanel from "./components/NoDataPanel.vue";
import PageToolbar from "./components/PageToolbar.vue";
import RawResultsPanel from "./components/RawResultsPanel.vue";
import SummaryTickerStrip from "./components/SummaryTickerStrip.vue";
import TickerRail from "./components/TickerRail.vue";
import { useDashboardData } from "./composables/useDashboardData";

const dashboard = useDashboardData();
</script>

<template>
  <main class="min-h-screen bg-[#0B0B0B]">
    <AppHeader
      :ingesting="dashboard.ingesting.value"
      :latest-date="dashboard.latestStoredDate.value"
      :selected-date="dashboard.selectedDate.value"
      :status="dashboard.status.value"
      @ingest="dashboard.runIngest"
      @select-latest="dashboard.selectLatestDate"
      @update:selected-date="dashboard.selectedDate.value = $event"
    />

    <div class="min-h-screen pt-16">
      <AppSidebar />
      <TickerRail
        :loading="dashboard.loading.value"
        :market-share="dashboard.marketShare.value"
        :products="dashboard.products.value"
        :results="dashboard.allResults.value"
        :summary="dashboard.summary.value"
        :units="dashboard.units.value"
      />

      <div class="min-w-0 lg:pl-16 2xl:pr-80">
        <div class="shell">
          <PageToolbar />

          <SummaryTickerStrip :loading="dashboard.loading.value" :summary="dashboard.summary.value" />

          <MarketPosition
            :error="dashboard.error.value"
            :loading="dashboard.loading.value"
            :rows="dashboard.marketShare.value"
            :status="dashboard.status.value"
            :units="dashboard.units.value"
            @refresh="dashboard.loadAll"
          />

          <NoDataPanel
            v-if="!dashboard.loading.value && !dashboard.error.value && !dashboard.hasStoredDataForDate.value"
            :ingesting="dashboard.ingesting.value"
            :latest-date="dashboard.latestStoredDate.value"
            :selected-date="dashboard.selectedDate.value"
            @ingest="dashboard.runIngest"
            @select-latest="dashboard.selectLatestDate"
          />

          <InsightStrip
            :results="dashboard.allResults.value"
            :loading="dashboard.loading.value"
            :market-share="dashboard.marketShare.value"
            :products="dashboard.products.value"
            :summary="dashboard.summary.value"
            :units="dashboard.units.value"
          />

          <AnalysisSection
            :loading="dashboard.loading.value"
            :products="dashboard.products.value"
            :timeseries="dashboard.timeseries.value"
          />

          <MarketComparisonTable :loading="dashboard.loading.value" :rows="dashboard.marketShare.value" />

          <RawResultsPanel
            :auction-product="dashboard.auctionProduct.value"
            :auction-unit="dashboard.auctionUnit.value"
            :has-results="dashboard.hasResults.value"
            :loading="dashboard.loading.value"
            :market-note="dashboard.marketInterpretation.value"
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
