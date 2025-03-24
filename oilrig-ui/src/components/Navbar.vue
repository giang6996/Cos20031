<template>
    <nav class="bg-gray-800 text-white px-6 py-4 shadow">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="text-xl font-semibold">🛢️ Oilrig Visual</div>
            <div class="flex sm:hidden">
            <button @click="menuOpen = !menuOpen" class="text-white focus:outline-none">
                <span v-if="!menuOpen">🟰</span>
                <span v-else>✕</span>
            </button>
            </div>
            <div class="hidden sm:flex sm:items-center sm:space-x-6">
            <Dropdown label="Oilrig">
                <RouterLink to="/oilrigs" class="dropdown-item">Oilrig List</RouterLink>
                <RouterLink to="/oilrigs/create" class="dropdown-item">Create Oilrigs</RouterLink>
            </Dropdown>

            <Dropdown label="Template">
                <RouterLink to="/templates" class="dropdown-item">Templates</RouterLink>
                <RouterLink to="/templates/create" class="dropdown-item">Create Template</RouterLink>
            </Dropdown>

            <Dropdown label="Report">
                <RouterLink to="/reports/upload" class="dropdown-item">Upload Report</RouterLink>
                <RouterLink to="/reports" class="dropdown-item">View Reports</RouterLink>
            </Dropdown>
            </div>
            
            <!-- <ul class="flex space-x-6 text-sm">
            <li><RouterLink to="/oilrigs" class="hover:text-teal-400">Oilrig List</RouterLink></li>
            <li><RouterLink to="/oilrigs/create" class="hover:text-teal-400">Create Oilrigs</RouterLink></li>
            <li><RouterLink to="/templates" class="hover:text-teal-400">Templates</RouterLink></li>
            <li><RouterLink to="/templates/create" class="hover:text-teal-400">Create Template</RouterLink></li>
            <li><RouterLink to="/reports/upload" class="hover:text-teal-400">Upload Report</RouterLink></li>
            <li><RouterLink to="/reports/view" class="hover:text-teal-400">View Reports</RouterLink></li>
            </ul> -->

            <!-- Mobile Dropdown -->
            <div v-if="menuOpen" class="sm:hidden flex flex-col space-y-2 mt-4">
                <Dropdown label="Oilrig" isMobile>
                    <RouterLink to="/oilrigs" class="dropdown-item">Oilrig List</RouterLink>
                    <RouterLink to="/oilrigs/create" class="dropdown-item">Create Oilrigs</RouterLink>
                </Dropdown>

                <Dropdown label="Template" isMobile>
                    <RouterLink to="/templates" class="dropdown-item">Templates</RouterLink>
                    <RouterLink to="/templates/create" class="dropdown-item">Create Template</RouterLink>
                </Dropdown>

                <Dropdown label="Report" isMobile>
                    <RouterLink to="/reports/upload" class="dropdown-item">Upload Report</RouterLink>
                    <RouterLink to="/reports" class="dropdown-item">View Reports</RouterLink>
                </Dropdown>
            </div>
      </div>
    </nav>
  </template>
  
<script setup>
    import { ref } from 'vue'
    import Dropdown from './NavDropdown.vue'
    import { RouterLink } from 'vue-router'

    const menuOpen = ref(false)
</script>

<style scoped>
.dropdown-item {
  display: block;
  padding: 0.5rem 1rem;
  color: white;
}
.dropdown-item:hover {
  background-color: #374151; /* Tailwind gray-700 */
}
</style>
  