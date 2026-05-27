<script setup lang="ts">
import { computed } from "vue";
import AppDatePicker from "./AppDatePicker.vue";
import BrandLogo from "./BrandLogo.vue";
import Icons from "./Icons.vue";

const props = defineProps<{
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

const updateStatus = computed(() => {
  if (props.ingesting) {
    return `Updating NESO results for ${props.selectedDate}.`;
  }

  return props.status;
});
</script>

<template>
  <header class="appHeader">
    <div class="appHeader__left">
      <BrandLogo />
      <nav class="topBreadcrumbs" aria-label="Breadcrumb">
        <span>NESO</span>
        <span>Auction Results</span>
        <strong>Ancillary Services</strong>
      </nav>
    </div>

    <div class="appHeader__right">
      <span class="headerStatus" aria-live="polite">{{ updateStatus }}</span>

      <div class="headerControls" aria-label="Dashboard controls">
        <button
          v-if="latestDate && latestDate !== selectedDate"
          class="subtleButton headerLatestButton"
          type="button"
          @click="emit('selectLatest')"
        >
          Latest
        </button>

        <AppDatePicker
          label="Delivery day"
          :model-value="selectedDate"
          @update:model-value="emit('update:selectedDate', $event)"
        />

        <button
          class="primaryButton headerUpdateButton"
          :disabled="ingesting"
          type="button"
          @click="emit('ingest')"
        >
          <Icons name="refresh" :class="ingesting ? 'animate-spin' : ''" :size="15" />
          {{ ingesting ? "Updating" : "Update" }}
        </button>
      </div>

      <div class="avatarButton">
        HE
      </div>
    </div>
  </header>
</template>
