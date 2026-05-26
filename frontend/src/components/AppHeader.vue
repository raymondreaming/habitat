<script setup lang="ts">
import BrandLogo from "./BrandLogo.vue";
</script>

<template>
  <header class="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 lg:px-6">
    <div class="flex min-w-0 items-center">
      <BrandLogo />
    </div>
    <div class="flex h-9 w-9 items-center justify-center rounded-full bg-slate-950 text-sm font-extrabold text-white shadow-sm">
      HE
    </div>
  </header>
</template>
