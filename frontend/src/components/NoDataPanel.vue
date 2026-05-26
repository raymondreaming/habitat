<script setup lang="ts">
import { RefreshCw } from "lucide-vue-next";

defineProps<{
  selectedDate: string;
  latestDate: string | null;
  ingesting: boolean;
}>();

const emit = defineEmits<{
  ingest: [];
  selectLatest: [];
}>();
</script>

<template>
  <section class="mb-5 rounded-lg border border-dashed border-slate-300 bg-white p-6 shadow-sm">
    <p class="text-xs font-extrabold uppercase text-slate-500">No results yet</p>
    <h2 class="mt-2 text-xl font-extrabold text-slate-950">No Habitat accepted results for {{ selectedDate }}</h2>
    <div class="mt-4 flex flex-col gap-3 sm:flex-row">
      <button
        class="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-slate-950 px-4 text-sm font-bold text-white disabled:cursor-wait disabled:opacity-65"
        :disabled="ingesting"
        type="button"
        @click="emit('ingest')"
      >
        <RefreshCw :size="17" />
        {{ ingesting ? "Updating" : "Update this day" }}
      </button>
      <button
        v-if="latestDate"
        class="inline-flex h-10 items-center justify-center rounded-md bg-slate-100 px-4 text-sm font-bold text-slate-950"
        type="button"
        @click="emit('selectLatest')"
      >
        View latest available day: {{ latestDate }}
      </button>
    </div>
  </section>
</template>
