<script setup lang="ts">
import Icons from "./Icons.vue";

defineProps<{
  selectedDate: string;
  ingesting: boolean;
  latestDate: string | null;
  status: string;
}>();

const emit = defineEmits<{
  "update:selectedDate": [value: string];
  ingest: [];
  selectLatest: [];
}>();
</script>

<template>
  <section class="commandBar">
    <div class="commandBar__copy">
      <h1>Ancillary Services Performance</h1>
      <p>Habitat cleared volume, price exposure, market share, and asset contribution by delivery day.</p>
    </div>

    <div class="commandBar__actions">
      <button
        v-if="latestDate && latestDate !== selectedDate"
        class="subtleButton"
        type="button"
        @click="emit('selectLatest')"
      >
        Latest {{ latestDate }}
      </button>

      <label class="dateControl">
        <span>Delivery day</span>
        <span class="relative">
          <Icons name="calendar" class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[#868F97]" :size="17" />
          <input
            class="pl-10"
            :value="selectedDate"
            type="date"
            @input="emit('update:selectedDate', ($event.target as HTMLInputElement).value)"
          />
        </span>
      </label>

      <div class="commandBar__update">
        <button
          class="primaryButton"
          :disabled="ingesting"
          type="button"
          @click="emit('ingest')"
        >
          <Icons name="refresh" :class="ingesting ? 'animate-spin' : ''" :size="17" />
          {{ ingesting ? "Updating" : "Update results" }}
        </button>
        <span v-if="status">{{ status }}</span>
      </div>
    </div>
  </section>
</template>
