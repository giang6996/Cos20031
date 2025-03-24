<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Weekly Oil & Gas Report (Real)</h1>
  
      <div class="mb-4 flex flex-wrap items-center gap-4">
        <div>
          <label class="font-semibold block">Start Date:</label>
          <input type="date" v-model="startDate" class="border px-2 py-1 rounded" />
        </div>
  
        <div>
          <label class="font-semibold block">End Date:</label>
          <input type="date" v-model="endDate" class="border px-2 py-1 rounded" />
        </div>
  
        <button
          @click="fetchWeeklyData"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 self-end"
        >
          Load Report
        </button>
      </div>
  
      <div v-if="loading" class="text-gray-500">Loading...</div>
      <div v-else-if="reports.length === 0" class="text-red-500">No data found for selected range.</div>
  
      <table v-else class="min-w-full bg-white rounded shadow overflow-hidden">
        <thead class="bg-gray-100 text-left">
          <tr>
            <th class="p-2">Oilrig</th>
            <th class="p-2">Date</th>
            <th class="p-2">Real Oil</th>
            <th class="p-2">Real Gas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(report, index) in reports" :key="index" class="border-t">
            <td class="p-2">{{ report.name }}</td>
            <td class="p-2">{{ report.report_date }}</td>
            <td class="p-2">{{ report.real_oil ?? '-' }}</td>
            <td class="p-2">{{ report.real_gas ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const startDate = ref('')
  const endDate = ref('')
  const reports = ref([])
  const loading = ref(false)
  
  const fetchWeeklyData = async () => {
    if (!startDate.value || !endDate.value) return
  
    loading.value = true
    reports.value = []
  
    try {
      const res = await axios.get('/api/reports/daily/weekly', {
        params: {
          start_date: startDate.value,
          end_date: endDate.value
        }
      })
      reports.value = res.data
    } catch (err) {
      console.error('Error fetching weekly report:', err)
    } finally {
      loading.value = false
    }
  }
  </script>
  