<template>
  <div class="chartSkeleton" aria-hidden="true">
    <span v-for="index in 5" :key="`line-${index}`" class="chartSkeleton__line"></span>
    <div class="chartSkeleton__bars">
      <span v-for="index in 8" :key="`bar-${index}`" :style="{ height: `${24 + index * 7}%` }"></span>
    </div>
  </div>
</template>
