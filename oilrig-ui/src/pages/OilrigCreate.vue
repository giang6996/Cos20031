<template>
  <form @submit.prevent="handleSubmit" class="max-w-xl mx-auto p-4 bg-white rounded-xl shadow space-y-4">
    <h2 class="text-2xl font-bold">Add New Oilrig</h2>

    <div>
      <label class="block font-semibold">Oilrig Name</label>
      <input v-model="form.name" type="text" class="input" required />
    </div>

    <div>
      <label class="block font-semibold">Report Email</label>
      <input v-model="form.report_email" type="email" class="input" required />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block font-semibold">Latitude</label>
        <input v-model="form.latitude" type="number" step="0.000001" class="input" required />
      </div>
      <div>
        <label class="block font-semibold">Longitude</label>
        <input v-model="form.longitude" type="number" step="0.000001" class="input" required />
      </div>
    </div>

    <div>
      <label class="block font-semibold">Select Template(s)</label>
      <select v-model="form.template_ids" multiple class="input h-32">
        <option
          v-for="template in templates"
          :key="template.id"
          :value="template.id"
        >
          {{ template.temp_name }}
        </option>
      </select>
    </div>

    <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const form = ref({
  name: '',
  report_email: '',
  latitude: '',
  longitude: '',
  template_ids: []
})

const templates = ref([])

onMounted(async () => {
  const res = await axios.get('/api/templates') // backend API to get all templates
  templates.value = res.data
})

const handleSubmit = async () => {
  try {
    const res = await axios.post('/api/oilrigs', form.value)
    alert('Oilrig saved successfully!')
    form.value = { name: '', report_email: '', latitude: '', longitude: '', template_ids: [] }
  } catch (err) {
    console.error(err)
    alert('Failed to save oilrig.')
  }
}
</script>

<style scoped>
.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  margin-top: 0.25rem;
}
</style>

  