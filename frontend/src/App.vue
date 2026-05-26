<script setup lang="ts">
import Chart from "chart.js/auto";
import { RefreshCw, Search, Zap } from "lucide-vue-next";
import { computed, nextTick, onMounted, ref, watch } from "vue";
import {
  type AuctionResult,
  type Options,
  type Summary,
  getOptions,
  getResults,
  getSummary,
  ingest,
} from "./api";

const selectedDate = ref(currentLondonDate());
const serviceType = ref("");
const auctionUnit = ref("");
const auctionProduct = ref("");
const results = ref<AuctionResult[]>([]);
const summary = ref<Summary | null>(null);
const options = ref<Options | null>(null);
const loading = ref(false);
const ingesting = ref(false);
const error = ref("");
const status = ref("");
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

const hasResults = computed(() => results.value.length > 0);

onMounted(loadAll);
watch([selectedDate, serviceType, auctionUnit, auctionProduct], loadAll);

async function loadAll() {
  loading.value = true;
  error.value = "";
  try {
    const [nextSummary, nextOptions, nextResults] = await Promise.all([
      getSummary(selectedDate.value),
      getOptions(selectedDate.value),
      getResults({
        date: selectedDate.value,
        serviceType: serviceType.value,
        auctionUnit: auctionUnit.value,
        auctionProduct: auctionProduct.value,
      }),
    ]);
    summary.value = nextSummary;
    options.value = nextOptions;
    results.value = nextResults.results;
    await nextTick();
    renderChart();
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : "Unable to load results.";
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
    status.value = `${run.records_upserted} records stored for ${run.target_date}.`;
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

function renderChart() {
  if (!chartCanvas.value || !summary.value) return;
  chart?.destroy();
  chart = new Chart(chartCanvas.value, {
    type: "bar",
    data: {
      labels: summary.value.by_service_type.map((item) => item.service_type),
      datasets: [
        {
          label: "MW",
          data: summary.value.by_service_type.map((item) => item.executed_quantity),
          backgroundColor: ["#0f766e", "#2563eb", "#9333ea", "#ea580c"],
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 },
        },
      },
    },
  });
}

function currentLondonDate() {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/London",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date());
  const lookup = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${lookup.year}-${lookup.month}-${lookup.day}`;
}
</script>

<template>
  <main class="shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">NESO auction results</p>
        <h1>Habitat Energy</h1>
      </div>
      <div class="actions">
        <label>
          <span>Date</span>
          <input v-model="selectedDate" type="date" />
        </label>
        <button :disabled="ingesting" type="button" @click="runIngest">
          <Zap :size="18" />
          {{ ingesting ? "Ingesting" : "Ingest" }}
        </button>
      </div>
    </header>

    <section class="metrics" aria-label="Summary">
      <article>
        <span>Records</span>
        <strong>{{ summary?.total_records ?? 0 }}</strong>
      </article>
      <article>
        <span>Total MW</span>
        <strong>{{ (summary?.total_executed_quantity ?? 0).toFixed(1) }}</strong>
      </article>
      <article>
        <span>Avg £/MW/h</span>
        <strong>{{ (summary?.average_clearing_price ?? 0).toFixed(2) }}</strong>
      </article>
    </section>

    <section class="panel">
      <div class="panelHeader">
        <div>
          <h2>Stored Results</h2>
          <p v-if="status" class="status">{{ status }}</p>
        </div>
        <button class="secondary" type="button" @click="loadAll">
          <RefreshCw :size="17" />
          Refresh
        </button>
      </div>

      <div class="filters">
        <label>
          <span>Service</span>
          <select v-model="serviceType">
            <option value="">All</option>
            <option v-for="value in options?.service_types" :key="value" :value="value">{{ value }}</option>
          </select>
        </label>
        <label>
          <span>Unit</span>
          <select v-model="auctionUnit">
            <option value="">All</option>
            <option v-for="value in options?.auction_units" :key="value" :value="value">{{ value }}</option>
          </select>
        </label>
        <label>
          <span>Product</span>
          <select v-model="auctionProduct">
            <option value="">All</option>
            <option v-for="value in options?.auction_products" :key="value" :value="value">{{ value }}</option>
          </select>
        </label>
        <button class="secondary" type="button" @click="clearFilters">
          <Search :size="17" />
          Clear
        </button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <div class="contentGrid">
        <div class="chartBox">
          <canvas ref="chartCanvas" aria-label="Cleared volume by service type"></canvas>
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
              <tr v-for="row in results" v-else :key="row.unit_result_id">
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
      </div>
    </section>
  </main>
</template>
