<template>
    <div class="relative" 
    @mouseenter="handleMouseEnter" 
    @mouseleave="handleMouseLeave"
    >
      <button @click="isMobile && (open = !open)" class="text-sm font-medium hover:text-teal-400">
        {{ label }}
      </button>
  
      <div
        v-if="open"
        class="absolute sm:absolute bg-gray-800 rounded shadow mt-2 z-10 w-50"
        :class="{ 'relative w-full mt-1': isMobile }"
      >
        <slot @click="handleClick" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  const props = defineProps({ label: String, isMobile: Boolean })
  const open = ref(false)
  let timeout = null

  const handleMouseEnter = () => {
    if (!props.isMobile) {
      clearTimeout(timeout)
      open.value = true
    }
  }

  const handleMouseLeave = () => {
    if (!props.isMobile) {
      timeout = setTimeout(() => {
        open.value = false
      }, 50) // slight delay to let click events go through
    }
  }

  const handleClick = () => {
    if (!props.isMobile) {
      open.value = false
    }
  }

  </script>
  