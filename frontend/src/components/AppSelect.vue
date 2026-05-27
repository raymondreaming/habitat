<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import Icons from "./Icons.vue";

const props = withDefaults(
  defineProps<{
    label: string;
    modelValue: string;
    options: string[];
    placeholder?: string;
    disabled?: boolean;
  }>(),
  {
    placeholder: "All",
    disabled: false,
  },
);

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const isOpen = ref(false);
const root = ref<HTMLElement | null>(null);

const selectedLabel = computed(() => props.modelValue || props.placeholder);
const optionCount = computed(() => props.options.length);

function toggle() {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
  }
}

function selectValue(value: string) {
  emit("update:modelValue", value);
  isOpen.value = false;
}

function onPointerDown(event: PointerEvent) {
  if (root.value && !root.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === "Escape") {
    isOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener("pointerdown", onPointerDown);
  document.addEventListener("keydown", onKeydown);
});

onBeforeUnmount(() => {
  document.removeEventListener("pointerdown", onPointerDown);
  document.removeEventListener("keydown", onKeydown);
});
</script>

<template>
  <div ref="root" class="appSelect" :class="{ 'appSelect--open': isOpen, 'appSelect--selected': modelValue }">
    <span class="appSelect__label">{{ label }}</span>
    <button
      class="appSelect__trigger"
      type="button"
      :aria-expanded="isOpen"
      :aria-label="`${label}: ${selectedLabel}`"
      :disabled="disabled"
      @click="toggle"
    >
      <span>{{ selectedLabel }}</span>
      <Icons name="chevronDown" :size="15" />
    </button>

    <div v-if="isOpen" class="appSelect__menu" role="listbox" :aria-label="label">
      <button
        class="appSelect__option"
        :class="{ 'appSelect__option--active': !modelValue }"
        type="button"
        role="option"
        :aria-selected="!modelValue"
        @click="selectValue('')"
      >
        <span>{{ placeholder }}</span>
        <Icons v-if="!modelValue" name="check" :size="14" />
      </button>

      <button
        v-for="option in options"
        :key="option"
        class="appSelect__option"
        :class="{ 'appSelect__option--active': option === modelValue }"
        type="button"
        role="option"
        :aria-selected="option === modelValue"
        @click="selectValue(option)"
      >
        <span>{{ option }}</span>
        <Icons v-if="option === modelValue" name="check" :size="14" />
      </button>

      <div v-if="!optionCount" class="appSelect__empty">No options</div>
    </div>
  </div>
</template>
