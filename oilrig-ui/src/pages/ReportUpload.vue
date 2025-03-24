<template>
    <div class="p-6 max-w-xl  mx-auto bg-white rounded shadow space-y-4">
      <h1 class="text-2xl font-bold">Upload Report</h1>
  
      <input type="file" accept=".xlsx, .xls" @change="handleFile" class="input" />
  
      <div v-if="loading">Uploading and processing...</div>
  
      <div v-if="result">
        <h2 class="font-semibold text-lg mt-4 mb-2">Extraction Result</h2>
        <pre class="bg-gray-100 p-3 rounded overflow-auto text-sm">{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const result = ref(null)
  const loading = ref(false)
  
  const handleFile = async (e) => {
    const file = e.target.files[0]
    if (!file) return
  
    const formData = new FormData()
    formData.append('report', file)
  
    loading.value = true
    result.value = null
  
    try {
      const res = await axios.post('/api/reports/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      result.value = res.data
    } catch (err) {
      console.error(err)
      result.value = { error: 'Upload failed or template not matched.' }
    } finally {
      loading.value = false
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
  