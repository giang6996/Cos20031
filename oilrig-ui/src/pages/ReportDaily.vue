<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Daily Oil Reports</h1>

    <div class="mb-4 flex items-center space-x-4">
      <label class="font-semibold">Select Date:</label>
      <input type="date" v-model="selectedDate" class="border px-2 py-1 rounded" />
      <button
        @click="fetchReports"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Load Reports
      </button>
    </div>

    <div v-if="loading" class="text-gray-500">Loading...</div>
    <div v-else-if="reports.length === 0" class="text-red-500">No reports found.</div>

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
          <td class="p-2">{{ report.real_oil }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedDate = ref('')
const reports = ref([])
const loading = ref(false)

const fetchReports = async () => {
  if (!selectedDate.value) return

  loading.value = true
  reports.value = []

  console.log("Requesting reports for", selectedDate.value)

  try {
    const res = await axios.get('/api/reports/daily', {
      params: { date: selectedDate.value }
    })
    reports.value = res.data
  } catch (err) {
    console.error('Error fetching reports:', err)
  } finally {
    loading.value = false
  }
}
</script>
