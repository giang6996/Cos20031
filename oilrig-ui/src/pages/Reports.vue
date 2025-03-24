<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-6">Available Report Types</h1>
  
      <div class="grid gap-4 md:grid-cols-2">
        <div
          v-for="(report, index) in reportTypes"
          :key="index"
          class="p-4 bg-white shadow rounded hover:bg-blue-50 transition cursor-pointer"
          @click="navigate(report.route)"
        >
          <h2 class="text-lg font-semibold">{{ report.title }}</h2>
          <p class="text-gray-600">{{ report.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const navigate = (path) => {
    router.push(path)
  }
  
  const reportTypes = [
    {
      title: 'Daily Production Summary',
      description: 'Create a daily production summary on a specific rigs.',
      route: '/reports/all'
    },
    {
      title: 'Daily Production (All Rigs)',
      description: 'Check daily real oil production across all oilrigs for a specific date.',
      route: '/reports/daily'
    },
    {
      title: 'Daily by Rig',
      description: 'View daily oil production for a specific rig.',
      route: '/reports/daily-rig-name'
    },
    {
      title: 'Weekly Real (Oil & Gas)',
      description: 'Compare real oil and gas production across a weekly range.',
      route: '/reports/weekly'
    },
    {
      title: 'Monthly Planned vs Real',
      description: 'Compare planned and real values for oil and gas in a selected month.',
      route: '/reports/monthly'
    },
    {
      title: 'Quarterly Summary',
      description: 'Summarize production over 3 months (quarter), planned vs actual.',
      route: '/reports/quarterly'
    },
    {
      title: 'Annual Summary',
      description: 'Compare planned and real production for a full year.',
      route: '/reports/annually'
    },
    {
      title: 'Daily vs Monthly Target (%)',
      description: 'Calculate daily production percentage compared to monthly target.',
      route: '/reports/percent-daily'
    },
    {
      title: 'Monthly Real vs Planned (%)',
      description: 'Percentage of monthly real oil vs monthly planned target.',
      route: '/reports/percent-monthly'
    },
    {
      title: 'Monthly Real vs Annual Target (%)',
      description: 'How each month performs against the yearly plan.',
      route: '/reports/percent-monthly-annually'
    },
    {
      title: 'Total Monthly vs Annual (%)',
      description: 'Total oil produced in months vs total planned annual oil.',
      route: '/reports/percent-yearly'
    },
  ]
  </script>
  