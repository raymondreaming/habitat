<script setup lang="ts">
import Icons from "./Icons.vue";

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
  <section class="emptyState">
    <div>
      <p>No results yet</p>
      <h2>No Habitat accepted results for {{ selectedDate }}</h2>
    </div>
    <div class="emptyState__actions">
      <button
        class="primaryButton"
        :disabled="ingesting"
        type="button"
        @click="emit('ingest')"
      >
        <Icons name="refresh" :size="17" />
        {{ ingesting ? "Updating" : "Update this day" }}
      </button>
      <button
        v-if="latestDate"
        class="subtleButton"
        type="button"
        @click="emit('selectLatest')"
      >
        View latest available day: {{ latestDate }}
      </button>
    </div>
  </section>
</template>
