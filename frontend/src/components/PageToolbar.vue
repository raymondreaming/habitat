<script setup lang="ts">
import { Zap } from "lucide-vue-next";

defineProps<{
  selectedDate: string;
  ingesting: boolean;
}>();

const emit = defineEmits<{
  "update:selectedDate": [value: string];
  ingest: [];
}>();
</script>

<template>
  <section class="mb-5 flex flex-col justify-between gap-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm lg:flex-row lg:items-end">
    <div>
      <p class="text-xs font-extrabold uppercase text-slate-500">NESO auction results</p>
      <h1 class="mt-1 text-2xl font-extrabold leading-tight text-slate-950">Market Performance</h1>
    </div>
    <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
      <label class="grid gap-1">
        <span class="text-xs font-bold text-slate-500">Delivery date</span>
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
        {{ ingesting ? "Ingesting" : "Ingest" }}
      </button>
    </div>
  </section>
</template>
