import { computed, onMounted, ref, shallowRef, watch } from "vue";
import {
  type AuctionResult,
  type MarketShare,
  type Options,
  type ProductPerformance,
  type Summary,
  type TimeSeriesPoint,
  type UnitPerformance,
  getMarketShare,
  getLatestDate,
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
  const results = shallowRef<AuctionResult[]>([]);
  const allResults = shallowRef<AuctionResult[]>([]);
  const summary = shallowRef<Summary | null>(null);
  const options = shallowRef<Options | null>(null);
  const marketShare = shallowRef<MarketShare[]>([]);
  const timeseries = shallowRef<TimeSeriesPoint[]>([]);
  const units = shallowRef<UnitPerformance[]>([]);
  const products = shallowRef<ProductPerformance[]>([]);
  const loading = ref(true);
  const ingesting = ref(false);
  const error = ref("");
  const status = ref("");
  const latestStoredDate = ref<string | null>(null);

  const hasResults = computed(() => results.value.length > 0);
  const hasStoredDataForDate = computed(() => (summary.value?.total_records ?? 0) > 0);
  const marketInterpretation = computed(() => {
    const strongestPosition = [...marketShare.value]
      .filter((row) => row.habitat_executed_quantity > 0)
      .sort((a, b) => b.habitat_market_share_percent - a.habitat_market_share_percent)[0];

    return strongestPosition
      ? `Habitat's strongest position was ${strongestPosition.service_type}, clearing ${strongestPosition.habitat_market_share_percent.toFixed(1)}% of accepted market volume.`
      : "";
  });

  onMounted(initializeDashboard);
  watch([selectedDate, serviceType, auctionUnit, auctionProduct], () => loadAll());

  async function initializeDashboard() {
    try {
      const latest = await getLatestDate();
      latestStoredDate.value = latest.date;
      if (latest.date && latest.date !== selectedDate.value) {
        selectedDate.value = latest.date;
        return;
      }
    } catch {
      // Fall back to the current London delivery date if the database is empty or unavailable.
    }
    await loadAll();
  }

  async function loadAll(loadOptions: { background?: boolean } = {}) {
    if (!loadOptions.background) {
      loading.value = true;
    }
    error.value = "";
    try {
      const hasFilters = Boolean(serviceType.value || auctionUnit.value || auctionProduct.value);
      const baseResultsRequest = getResults({ date: selectedDate.value });
      const filteredResultsRequest = hasFilters
        ? getResults({
            date: selectedDate.value,
            serviceType: serviceType.value,
            auctionUnit: auctionUnit.value,
            auctionProduct: auctionProduct.value,
          })
        : baseResultsRequest;
      const [
        nextSummary,
        nextOptions,
        nextAllResults,
        nextResults,
        nextMarketShare,
        nextTimeseries,
        nextUnits,
        nextProducts,
      ] = await Promise.all([
        getSummary(selectedDate.value),
        getOptions(selectedDate.value),
        baseResultsRequest,
        filteredResultsRequest,
        getMarketShare(selectedDate.value),
        getTimeseries(selectedDate.value),
        getUnits(selectedDate.value),
        getProducts(selectedDate.value),
      ]);
      summary.value = nextSummary;
      options.value = nextOptions;
      allResults.value = nextAllResults.results;
      results.value = nextResults.results;
      marketShare.value = nextMarketShare.market_share;
      timeseries.value = nextTimeseries.timeseries;
      units.value = nextUnits.units;
      products.value = nextProducts.products;
    } catch (loadError) {
      error.value = loadError instanceof Error ? loadError.message : "Unable to load market performance data.";
    } finally {
      if (!loadOptions.background) {
        loading.value = false;
      }
    }
  }

  async function runIngest() {
    ingesting.value = true;
    error.value = "";
    status.value = `Updating NESO auction results for ${selectedDate.value}.`;
    try {
      const run = await ingest(selectedDate.value);
      latestStoredDate.value = run.target_date;
      status.value =
        run.records_upserted > 0
          ? `Updated ${run.records_upserted} Habitat results for ${run.target_date}.`
          : `No Habitat accepted results found for ${run.target_date}.`;
      await loadAll({ background: true });
    } catch (ingestError) {
      error.value = ingestError instanceof Error ? ingestError.message : "Unable to update results.";
      status.value = `Update failed for ${selectedDate.value}.`;
    } finally {
      ingesting.value = false;
    }
  }

  function clearFilters() {
    serviceType.value = "";
    auctionUnit.value = "";
    auctionProduct.value = "";
  }

  function selectLatestDate() {
    if (latestStoredDate.value) {
      selectedDate.value = latestStoredDate.value;
    }
  }

  return {
    selectedDate,
    serviceType,
    auctionUnit,
    auctionProduct,
    results,
    allResults,
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
    latestStoredDate,
    hasResults,
    hasStoredDataForDate,
    marketInterpretation,
    loadAll,
    runIngest,
    clearFilters,
    selectLatestDate,
  };
}
