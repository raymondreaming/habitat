<script setup lang="ts">
import { computed } from "vue";
import type { UnitPerformance } from "../api";

const props = defineProps<{
  units: UnitPerformance[];
}>();

const topUnits = computed(() => props.units.slice(0, 8));
</script>

<template>
  <article class="panel leaderboard">
    <h2>Top Units</h2>
    <ol>
      <li v-for="unit in topUnits" :key="unit.auction_unit">
        <span>{{ unit.auction_unit }}</span>
        <strong>{{ unit.executed_quantity.toFixed(0) }} MW</strong>
      </li>
    </ol>
  </article>
</template>
