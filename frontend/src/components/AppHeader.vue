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
  <header class="topbar">
    <div>
      <p class="eyebrow">Market performance cockpit</p>
      <h1>Habitat Energy</h1>
    </div>
    <div class="actions">
      <label>
        <span>Date</span>
        <input :value="selectedDate" type="date" @input="emit('update:selectedDate', ($event.target as HTMLInputElement).value)" />
      </label>
      <button :disabled="ingesting" type="button" @click="emit('ingest')">
        <Zap :size="18" />
        {{ ingesting ? "Ingesting" : "Ingest" }}
      </button>
    </div>
  </header>
</template>
