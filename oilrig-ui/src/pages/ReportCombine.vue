<template>
    <div class="p-6">
      <h1 class="text-3xl font-bold mb-6">Oilrig Production Summary Dashboard</h1>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div>
          <label class="block font-semibold mb-1">Oilrig Name</label>
          <input v-model="rigName" type="text" class="input w-full" placeholder="e.g. Rig A" />
        </div>
        <div>
          <label class="block font-semibold mb-1">Year</label>
          <input v-model.number="year" type="number" min="2000" max="2100" class="input w-full" />
        </div>
        <div>
          <label class="block font-semibold mb-1">Month</label>
          <select v-model.number="month" class="input w-full">
            <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>
  
      <button
        @click="loadCombinedReport"
        class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 mb-6"
      >
        Load Summary
      </button>
  
      <div v-if="loading" class="text-gray-500">Loading...</div>
  
      <div v-else-if="summaryData">
        <h2 class="text-xl font-semibold mb-2">Summary for {{ rigName }} - {{ year }}/{{ month }}</h2>
        <table class="min-w-full bg-white rounded shadow overflow-hidden">
          <thead class="bg-gray-100">
            <tr>
              <th class="p-2">Metric</th>
              <th class="p-2">Oil</th>
              <th class="p-2">Gas</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="p-2 font-medium">Daily Real ({{ dailyDate }})</td>
              <td class="p-2">{{ summaryData.daily_oil ?? '-' }}</td>
              <td class="p-2">{{ summaryData.daily_gas ?? '-' }}</td>
            </tr>
            <tr>
              <td class="p-2 font-medium">Monthly Real</td>
              <td class="p-2">{{ summaryData.monthly_real_oil ?? '-' }}</td>
              <td class="p-2">{{ summaryData.monthly_real_gas ?? '-' }}</td>
            </tr>
            <tr>
              <td class="p-2 font-medium">Monthly Planned</td>
              <td class="p-2">{{ summaryData.monthly_planned_oil ?? '-' }}</td>
              <td class="p-2">{{ summaryData.monthly_planned_gas ?? '-' }}</td>
            </tr>
            <tr>
              <td class="p-2 font-medium">Annual Planned</td>
              <td class="p-2">{{ summaryData.annual_planned_oil ?? '-' }}</td>
              <td class="p-2">{{ summaryData.annual_planned_gas ?? '-' }}</td>
            </tr>
            <tr>
              <td class="p-2 font-medium">% Monthly Completion</td>
              <td class="p-2">{{ summaryData.percent_monthly_oil ?? '-' }}</td>
              <td class="p-2">{{ summaryData.percent_monthly_gas ?? '-' }}</td>
            </tr>
            <tr>
              <td class="p-2 font-medium">% Yearly Completion</td>
              <td class="p-2">{{ summaryData.percent_yearly_oil ?? '-' }}</td>
              <td class="p-2">{{ summaryData.percent_yearly_gas ?? '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const rigName = ref('')
  const year = ref(new Date().getFullYear())
  const month = ref(new Date().getMonth() + 1)
  const loading = ref(false)
  const summaryData = ref(null)
  const dailyDate = ref(new Date().toISOString().substring(0, 10))
  
  const loadCombinedReport = async () => {
    if (!rigName.value || !year.value || !month.value) return
    loading.value = true
    summaryData.value = null
  
    try {
      const [daily, monthly, percentMonthly, annual, percentYearly] = await Promise.all([
        axios.get('/api/reports/daily/by-rig', { params: { name: rigName.value } }),
        axios.get('/api/reports/monthly', { params: { year: year.value, month: month.value } }),
        axios.get('/api/reports/percent/monthly', { params: { year: year.value, month: month.value } }),
        axios.get('/api/reports/annually', { params: { year: year.value } }),
        axios.get('/api/reports/percent/monthly-vs-annual', { params: { year: year.value, month: month.value } })
      ])
  
      const latestDaily = daily.data.find(r => r.name === rigName.value)
      const monthlyRow = monthly.data.find(r => r.name === rigName.value)
      const percentMonth = percentMonthly.data.find(r => r.name === rigName.value)
      const annualRow = annual.data.find(r => r.name === rigName.value)
      const percentYear = percentYearly.data.find(r => r.name === rigName.value)
  
      summaryData.value = {
        daily_oil: latestDaily?.real_oil,
        daily_gas: latestDaily?.real_gas, // Null for now as query in backend does not retrieve gas data
        monthly_real_oil: monthlyRow?.real_oil,
        monthly_real_gas: monthlyRow?.real_gas,
        monthly_planned_oil: monthlyRow?.planned_oil,
        monthly_planned_gas: monthlyRow?.planned_gas,
        annual_planned_oil: annualRow?.planned_oil,
        annual_planned_gas: annualRow?.planned_gas,
        percent_monthly_oil: percentMonth?.oil_production_percentage?.toFixed(1) + '%',
        percent_monthly_gas: null, // Optional: add if needed
        percent_yearly_oil: percentYear?.oil_production_percentage?.toFixed(1) + '%',
        percent_yearly_gas: null // Optional
      }
    } catch (err) {
      console.error('Failed to load combined report:', err)
    } finally {
      loading.value = false
    }
  }
  </script>
  
  