import { computed, onMounted, ref, watch } from "vue";
import {
  type AuctionResult,
  type MarketShare,
  type Options,
  type ProductPerformance,
  type Summary,
  type TimeSeriesPoint,
  type UnitPerformance,
  getMarketShare,
  getOptions,
  getProducts,
  getResults,
  getSummary,
  getTimeseries,
  getUnits,
  ingest,
} from "../api";
import { currentLondonDate } from "../utils/date";

export function useDashboardData() {
  const selectedDate = ref(currentLondonDate());
  const serviceType = ref("");
  const auctionUnit = ref("");
  const auctionProduct = ref("");
  const results = ref<AuctionResult[]>([]);
  const summary = ref<Summary | null>(null);
  const options = ref<Options | null>(null);
  const marketShare = ref<MarketShare[]>([]);
  const timeseries = ref<TimeSeriesPoint[]>([]);
  const units = ref<UnitPerformance[]>([]);
  const products = ref<ProductPerformance[]>([]);
  const loading = ref(false);
  const ingesting = ref(false);
  const error = ref("");
  const status = ref("");

  const hasResults = computed(() => results.value.length > 0);

  onMounted(loadAll);
  watch([selectedDate, serviceType, auctionUnit, auctionProduct], loadAll);

  async function loadAll() {
    loading.value = true;
    error.value = "";
    try {
      const [nextSummary, nextOptions, nextResults, nextMarketShare, nextTimeseries, nextUnits, nextProducts] =
        await Promise.all([
          getSummary(selectedDate.value),
          getOptions(selectedDate.value),
          getResults({
            date: selectedDate.value,
            serviceType: serviceType.value,
            auctionUnit: auctionUnit.value,
            auctionProduct: auctionProduct.value,
          }),
          getMarketShare(selectedDate.value),
          getTimeseries(selectedDate.value),
          getUnits(selectedDate.value),
          getProducts(selectedDate.value),
        ]);
      summary.value = nextSummary;
      options.value = nextOptions;
      results.value = nextResults.results;
      marketShare.value = nextMarketShare.market_share;
      timeseries.value = nextTimeseries.timeseries;
      units.value = nextUnits.units;
      products.value = nextProducts.products;
    } catch (loadError) {
      error.value = loadError instanceof Error ? loadError.message : "Unable to load market performance data.";
    } finally {
      loading.value = false;
    }
  }

  async function runIngest() {
    ingesting.value = true;
    error.value = "";
    status.value = "";
    try {
      const run = await ingest(selectedDate.value);
      status.value = `${run.records_upserted} Habitat records stored for ${run.target_date}.`;
      await loadAll();
    } catch (ingestError) {
      error.value = ingestError instanceof Error ? ingestError.message : "Unable to run ingestion.";
    } finally {
      ingesting.value = false;
    }
  }

  function clearFilters() {
    serviceType.value = "";
    auctionUnit.value = "";
    auctionProduct.value = "";
  }

  return {
    selectedDate,
    serviceType,
    auctionUnit,
    auctionProduct,
    results,
    summary,
    options,
    marketShare,
    timeseries,
    units,
    products,
    loading,
    ingesting,
    error,
    status,
    hasResults,
    loadAll,
    runIngest,
    clearFilters,
  };
}
