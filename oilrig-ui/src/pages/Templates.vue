<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Templates</h1>
  
      <div v-if="loading">Loading templates...</div>
  
      <div v-else>
        <table class="w-full table-auto border-collapse bg-white shadow rounded">
          <thead>
            <tr class="bg-gray-100 text-left text-sm">
              <th class="px-4 py-2 border">Template Name</th>
              <th class="px-4 py-2 border">Check Cells</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="template in templates" :key="template.id" class="hover:bg-gray-50">
              <td class="px-4 py-2 border font-medium">{{ template.temp_name }}</td>
              <td class="px-4 py-2 border">
                <ul style="list-style-type: none">
                  <li v-for="check in template.checks" :key="check.id">
                    <code class="font-mono bg-gray-100 px-1 py-0.5 rounded">{{ check.check_cell }}</code>:
                    {{ check.check_value }}
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const templates = ref([])
  const loading = ref(true)
  
  onMounted(async () => {
    try {
      const res = await axios.get('/api/read/templates') // or whatever endpoint gives you template with checks
      templates.value = res.data
    } catch (err) {
      console.error('Failed to load templates:', err)
    } finally {
      loading.value = false
    }
  })
  </script>
  