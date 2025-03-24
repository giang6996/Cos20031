<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Oilrig List</h1>
  
      <div v-if="loading">Loading oilrigs...</div>
  
      <table v-else class="w-full table-auto border-collapse bg-white rounded shadow">
        <thead class="bg-gray-100 text-left">
          <tr>
            <th class="px-4 py-2 border">Name</th>
            <th class="px-4 py-2 border">Email</th>
            <th class="px-4 py-2 border">Coordinates</th>
            <!-- <th class="px-4 py-2 border">Templates</th> -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="rig in oilrigs" :key="rig.id" class="hover:bg-gray-50">
            <td class="px-4 py-2 border">{{ rig.name }}</td>
            <td class="px-4 py-2 border">{{ rig.report_email }}</td>
            <td class="px-4 py-2 border">
              {{ rig.latitude }}, {{ rig.longitude }}
            </td>
            <!-- <td class="px-4 py-2 border">
              <ul class="list-disc list-inside text-sm">
                <li v-for="template in rig.templates" :key="template.id">
                  {{ template.temp_name }}
                </li>
              </ul>
            </td> -->
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const oilrigs = ref([])
  const loading = ref(true)
  
  onMounted(async () => {
    try {
      const res = await axios.get('/api/read/oilrigs')
      oilrigs.value = res.data
    } catch (err) {
      console.error('Failed to load oilrigs:', err)
    } finally {
      loading.value = false
    }
  })
  </script>
  