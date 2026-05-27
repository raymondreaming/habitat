<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import Icons from "./Icons.vue";

const props = defineProps<{
  label: string;
  modelValue: string;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const weekdayLabels = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
const displayFormatter = new Intl.DateTimeFormat("en-US", { month: "2-digit", day: "2-digit", year: "numeric" });
const monthFormatter = new Intl.DateTimeFormat("en-US", { month: "long", year: "numeric" });

const root = ref<HTMLElement | null>(null);
const isOpen = ref(false);
const visibleMonth = ref(startOfMonth(parseDateValue(props.modelValue)));

const selectedDate = computed(() => parseDateValue(props.modelValue));
const displayDate = computed(() => displayFormatter.format(selectedDate.value));
const visibleMonthLabel = computed(() => monthFormatter.format(visibleMonth.value));

const calendarDays = computed(() => {
  const firstOfMonth = startOfMonth(visibleMonth.value);
  const start = new Date(firstOfMonth);
  start.setDate(firstOfMonth.getDate() - firstOfMonth.getDay());

  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    return {
      date,
      value: formatDateValue(date),
      isCurrentMonth: date.getMonth() === visibleMonth.value.getMonth(),
      isSelected: sameDay(date, selectedDate.value),
      isToday: sameDay(date, new Date()),
    };
  });
});

watch(
  () => props.modelValue,
  (value) => {
    visibleMonth.value = startOfMonth(parseDateValue(value));
  },
);

function parseDateValue(value: string) {
  const [year, month, day] = value.split("-").map(Number);
  if (!year || !month || !day) return new Date();
  return new Date(year, month - 1, day);
}

function formatDateValue(date: Date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function startOfMonth(date: Date) {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

function sameDay(a: Date, b: Date) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}

function moveMonth(offset: number) {
  visibleMonth.value = new Date(visibleMonth.value.getFullYear(), visibleMonth.value.getMonth() + offset, 1);
}

function selectDate(value: string) {
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
  <div ref="root" class="appDatePicker" :class="{ 'appDatePicker--open': isOpen }">
    <span class="appDatePicker__label">{{ label }}</span>
    <button
      class="appDatePicker__trigger"
      type="button"
      :aria-expanded="isOpen"
      :aria-label="`${label}: ${displayDate}`"
      @click="isOpen = !isOpen"
    >
      <Icons name="calendar" :size="15" />
      <span>{{ displayDate }}</span>
      <Icons name="chevronDown" :size="15" />
    </button>

    <div v-if="isOpen" class="appDatePicker__popover" role="dialog" :aria-label="label">
      <div class="appDatePicker__month">
        <button type="button" aria-label="Previous month" @click="moveMonth(-1)">
          <Icons name="chevronLeft" :size="15" />
        </button>
        <strong>{{ visibleMonthLabel }}</strong>
        <button type="button" aria-label="Next month" @click="moveMonth(1)">
          <Icons name="chevronRight" :size="15" />
        </button>
      </div>

      <div class="appDatePicker__weekdays">
        <span v-for="day in weekdayLabels" :key="day">{{ day }}</span>
      </div>

      <div class="appDatePicker__grid">
        <button
          v-for="day in calendarDays"
          :key="day.value"
          class="appDatePicker__day"
          :class="{
            'appDatePicker__day--outside': !day.isCurrentMonth,
            'appDatePicker__day--selected': day.isSelected,
            'appDatePicker__day--today': day.isToday,
          }"
          type="button"
          @click="selectDate(day.value)"
        >
          {{ day.date.getDate() }}
        </button>
      </div>
    </div>
  </div>
</template>
