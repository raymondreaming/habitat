<script setup lang="ts">
import Icons from "./Icons.vue";

defineProps<{
  modelValue: string;
  modes: ReadonlyArray<{
    id: string;
    label: string;
    icon: string;
    tooltip: string;
  }>;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <div class="chartModeSwitcher" aria-label="Analysis lens">
    <button
      v-for="mode in modes"
      :key="mode.id"
      class="chartModeButton"
      :class="{ 'chartModeButton--active': mode.id === modelValue }"
      type="button"
      :aria-pressed="mode.id === modelValue"
      :title="mode.tooltip"
      @click="emit('update:modelValue', mode.id)"
    >
      <Icons :name="mode.icon as any" :size="14" />
      <span>{{ mode.label }}</span>
    </button>
  </div>
</template>
