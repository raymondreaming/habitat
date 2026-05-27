<script setup lang="ts">
import LoadingSpinner from "./LoadingSpinner.vue";

defineProps<{
  label?: string;
}>();
</script>

<template>
  <div class="loadingState">
    <div class="flex items-center gap-2">
      <LoadingSpinner />
      <span>{{ label ?? "Loading results" }}</span>
    </div>
  </div>
</template>
