<script setup lang="ts">
import LoadingSpinner from "./LoadingSpinner.vue";

defineProps<{
  label?: string;
}>();
</script>

<template>
  <div class="flex min-h-40 items-center justify-center rounded-lg border border-slate-200 bg-white text-sm font-semibold text-slate-500">
    <div class="flex items-center gap-2">
      <LoadingSpinner />
      <span>{{ label ?? "Loading results" }}</span>
    </div>
  </div>
</template>
