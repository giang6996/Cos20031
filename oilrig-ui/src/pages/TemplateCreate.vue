<template>
    <div class="p-6 max-w-xl  mx-auto bg-white rounded shadow space-y-6">
      <h1 class="text-2xl font-bold">Create New Template</h1>
  
      <!-- Template Name -->
      <div>
        <label class="font-semibold block mb-1">Template Name</label>
        <input v-model="form.temp_name" class="input" />
      </div>
  
      <!-- Check Cells -->
      <div>
        <label class="font-semibold block mb-2">Check Cells</label>
        <div v-for="(check, index) in form.checks" :key="index" class="grid grid-cols-2 gap-4 mb-2">
          <input v-model="check.check_cell" class="input" placeholder="Cell (e.g. A1)" />
          <input v-model="check.check_value" class="input" placeholder="Expected Value" />
        </div>
        <button @click="addCheck" class="text-sm text-blue-600 hover:underline">+ Add Check</button>
      </div>
  
      <!-- Data Locations -->
      <div>
        <label class="font-semibold block mb-2">Data Cells</label>
        <div
          v-for="(data, index) in form.data_locations"
          :key="index"
          class="grid grid-cols-4 gap-4 mb-2"
        >
          <input v-model="data.data_cell" class="input" placeholder="Cell (e.g. C3)" />
          <select v-model="data.report_type" class="input">
            <option value="daily">Daily</option>
            <option value="monthly">Monthly</option>
            <option value="annually">Annually</option>
          </select>
          <select v-model="data.resource_type" class="input">
            <option value="oil">Oil</option>
            <option value="gas">Gas</option>
          </select>
          <select v-model="data.data_type" class="input">
            <option value="real">Real</option>
            <option value="planned">Planned</option>
          </select>
        </div>
        <button @click="addDataLocation" class="text-sm text-blue-600 hover:underline">+ Add Data</button>
      </div>
  
      <!-- Assign to Oilrigs -->
      <div>
        <label class="font-semibold block mb-2">Assign to Oilrig(s)</label>
        <select v-model="form.oilrig_ids" multiple class="input h-32">
          <option v-for="rig in oilrigs" :key="rig.id" :value="rig.id">
            {{ rig.name }}
          </option>
        </select>
      </div>
  
      <!-- Submit -->
      <div>
        <button @click="submitForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Save Template
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const form = ref({
    temp_name: '',
    checks: [{ check_cell: '', check_value: '' }],
    data_locations: [
      { data_cell: '', report_type: 'daily', resource_type: 'oil', data_type: 'real' }
    ],
    oilrig_ids: []
  })
  
  const oilrigs = ref([])
  
  onMounted(async () => {
    const res = await axios.get('/api/oilrigs')
    oilrigs.value = res.data
  })
  
  const addCheck = () => {
    form.value.checks.push({ check_cell: '', check_value: '' })
  }
  
  const addDataLocation = () => {
    form.value.data_locations.push({
      data_cell: '',
      report_type: 'daily',
      resource_type: 'oil',
      data_type: 'real'
    })
  }
  
  const submitForm = async () => {
    try {
      await axios.post('/api/templates/full-create', form.value)
      alert('Template created and linked successfully!')
      form.value = {
        temp_name: '',
        checks: [{ check_cell: '', check_value: '' }],
        data_locations: [
          { data_cell: '', report_type: 'daily', resource_type: 'oil', data_type: 'real' }
        ],
        oilrig_ids: []
      }
    } catch (err) {
      console.error(err)
      alert('Failed to create template.')
    }
  }
  </script>
  
  <style scoped>
  .input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
  }
  </style>
  