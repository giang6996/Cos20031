<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Monthly Planned vs Real Report</h1>
  
      <div class="mb-4 flex items-center space-x-4">
        <label class="font-semibold">Select Year:</label>
        <input type="number" v-model.number="year" class="border px-2 py-1 rounded" min="2000" max="2100" />
  
        <label class="font-semibold">Month:</label>
        <select v-model.number="month" class="border px-2 py-1 rounded">
          <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
        </select>
  
        <button
          @click="fetchReports"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Load Report
        </button>
      </div>
  
      <div v-if="loading" class="text-gray-500">Loading...</div>
      <div v-else-if="reports.length === 0" class="text-red-500">No data found for selected month.</div>
  
      <table v-else class="min-w-full bg-white rounded shadow overflow-hidden">
        <thead class="bg-gray-100 text-left">
          <tr>
            <th class="p-2">Oilrig</th>
            <th class="p-2">Date</th>
            <th class="p-2">Planned Oil</th>
            <th class="p-2">Real Oil</th>
            <th class="p-2">Planned Gas</th>
            <th class="p-2">Real Gas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(report, index) in reports" :key="index" class="border-t">
            <td class="p-2">{{ report.name }}</td>
            <td class="p-2">{{ report.report_date }}</td>
            <td class="p-2">{{ report.planned_oil ?? '-' }}</td>
            <td class="p-2">{{ report.real_oil ?? '-' }}</td>
            <td class="p-2">{{ report.planned_gas ?? '-' }}</td>
            <td class="p-2">{{ report.real_gas ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const year = ref(new Date().getFullYear())
  const month = ref(new Date().getMonth() + 1)
  const reports = ref([])
  const loading = ref(false)
  
  const fetchReports = async () => {
    loading.value = true
    reports.value = []
    try {
      const res = await axios.get('/api/reports/monthly', {
        params: { year: year.value, month: month.value }
      })
      reports.value = res.data
    } catch (err) {
      console.error('Error fetching monthly report:', err)
    } finally {
      loading.value = false
    }
  }
  </script>
  