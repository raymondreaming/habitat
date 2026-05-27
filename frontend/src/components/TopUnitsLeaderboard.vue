<script setup lang="ts">
import { computed } from "vue";
import type { UnitPerformance } from "../api";
import { currency } from "../utils/format";
import Icons from "./Icons.vue";

const props = defineProps<{
  loading: boolean;
  units: UnitPerformance[];
}>();

const topUnits = computed(() => [...props.units].sort((a, b) => b.estimated_gross_revenue - a.estimated_gross_revenue).slice(0, 8));
const maxValue = computed(() => Math.max(...topUnits.value.map((unit) => unit.estimated_gross_revenue), 1));

function valueWidth(unit: UnitPerformance) {
  return `${Math.max((unit.estimated_gross_revenue / maxValue.value) * 100, 3)}%`;
}
</script>

<template>
  <article class="leaderboardPanel">
    <div class="leaderboardPanel__header">
      <h2>Top Units</h2>
    </div>
    <ol>
      <template v-if="loading">
        <li v-for="index in 8" :key="index" class="unitRankRow unitRankRow--loading">
          <span class="unitRankRow__rank">{{ String(index).padStart(2, "0") }}</span>
          <span class="unitRankRow__icon">
            <Icons name="zap" :size="15" />
          </span>
          <span class="unitRankRow__asset"><i></i></span>
          <span class="unitRankRow__bar"><span></span></span>
          <strong>
            <i></i>
            <small><i></i></small>
          </strong>
        </li>
      </template>
      <template v-else>
        <li
          v-for="(unit, index) in topUnits"
          :key="unit.auction_unit"
          class="unitRankRow"
          v-memo="[unit.executed_quantity, unit.estimated_gross_revenue]"
        >
          <span class="unitRankRow__rank">{{ String(index + 1).padStart(2, "0") }}</span>
          <span class="unitRankRow__icon">
            <Icons name="zap" :size="15" />
          </span>
          <span class="unitRankRow__asset">{{ unit.auction_unit }}</span>
          <span class="unitRankRow__bar" aria-hidden="true">
            <span :style="{ width: valueWidth(unit) }"></span>
          </span>
          <strong>
            {{ currency(unit.estimated_gross_revenue) }}
            <small>{{ unit.executed_quantity.toFixed(0) }} MW</small>
          </strong>
        </li>
      </template>
    </ol>
  </article>
</template>
