<script setup lang="ts">
import { Zap } from "lucide-vue-next";

defineProps<{
  selectedDate: string;
  ingesting: boolean;
  loading: boolean;
  latestDate: string | null;
  status: string;
  hasStoredData: boolean;
}>();

const emit = defineEmits<{
  "update:selectedDate": [value: string];
  ingest: [];
  selectLatest: [];
}>();
</script>

<template>
  <section class="mb-5 flex flex-col justify-between gap-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm lg:flex-row lg:items-end">
    <div>
      <p class="text-xs font-extrabold uppercase text-slate-500">Auction results</p>
      <h1 class="mt-1 text-2xl font-extrabold leading-tight text-slate-950">Daily Market Performance</h1>
      <div class="mt-3 flex flex-wrap items-center gap-2">
        <span
          class="rounded-full px-2.5 py-1 text-xs font-bold"
          :class="hasStoredData ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'"
        >
          {{ loading ? "Loading results" : hasStoredData ? "Results ready" : "No results for selected day" }}
        </span>
        <button
          v-if="latestDate && latestDate !== selectedDate"
          class="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-bold text-slate-700"
          type="button"
          @click="emit('selectLatest')"
        >
          Latest available: {{ latestDate }}
        </button>
        <span v-if="status" class="text-sm font-semibold text-emerald-700">{{ status }}</span>
      </div>
    </div>
    <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
      <label class="grid gap-1">
        <span class="text-xs font-bold text-slate-500">Delivery day</span>
        <input
          class="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm text-slate-950"
          :value="selectedDate"
          type="date"
          @input="emit('update:selectedDate', ($event.target as HTMLInputElement).value)"
        />
      </label>
      <button
        class="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-slate-950 px-4 text-sm font-bold text-white disabled:cursor-wait disabled:opacity-65"
        :disabled="ingesting"
        type="button"
        @click="emit('ingest')"
      >
        <Zap :size="18" />
        {{ ingesting ? "Updating" : "Update results" }}
      </button>
    </div>
  </section>
</template>
