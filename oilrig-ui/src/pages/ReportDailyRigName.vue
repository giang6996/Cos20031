<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Daily Oil Report by Rig</h1>
  
      <div class="mb-4 flex flex-wrap items-center gap-4">
        <label class="font-semibold">Oilrig Name:</label>
        <input v-model="rigName" type="text" class="border px-2 py-1 rounded" placeholder="Enter oilrig name..." />
  
        <button
          @click="fetchByRig"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Load Reports
        </button>
      </div>
  
      <div v-if="loading" class="text-gray-500">Loading...</div>
      <div v-else-if="reports.length === 0" class="text-red-500">No data found for that rig.</div>
  
      <table v-else class="min-w-full bg-white rounded shadow overflow-hidden">
        <thead class="bg-gray-100 text-left">
          <tr>
            <th class="p-2">Oilrig</th>
            <th class="p-2">Date</th>
            <th class="p-2">Real Oil</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(report, index) in reports" :key="index" class="border-t">
            <td class="p-2">{{ report.name }}</td>
            <td class="p-2">{{ report.report_date }}</td>
            <td class="p-2">{{ report.real_oil ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const rigName = ref('')
  const reports = ref([])
  const loading = ref(false)
  
  const fetchByRig = async () => {
    if (!rigName.value) return
  
    loading.value = true
    reports.value = []
  
    try {
      const res = await axios.get('/api/reports/daily/by-rig', {
        params: { name: rigName.value }
      })
      reports.value = res.data
    } catch (err) {
      console.error('Error fetching by-rig report:', err)
    } finally {
      loading.value = false
    }
  }
  </script>
  