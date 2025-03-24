import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

const mock = new MockAdapter(axios, { delayResponse: 300 }) // optional delay to simulate loading

// Mock oilrigs 

mock.onGet('/api/oilrigs-with-templates').reply(200, [
  {
    "id": 1,
    "name": "Alpha Rig",
    "report_email": "alpha@rig.com",
    "latitude": 12.345,
    "longitude": 98.765,
    "templates": [
      { "id": 1, "temp_name": "Daily Oil Template" },
      { "id": 2, "temp_name": "Monthly Summary Template" }
    ]
  },
  {
    "id": 2,
    "name": "Bravo Rig",
    "report_email": "bravo@rig.com",
    "latitude": 23.456,
    "longitude": 87.654,
    "templates": []
  }
])


// Mock templates-with-checks
mock.onGet('/api/templates-with-checks').reply(200, [
  {
    id: 1,
    temp_name: 'Template A',
    checks: [
      { id: 1, check_cell: 'B2', check_value: 'Hello' },
      { id: 2, check_cell: 'C5', check_value: 'World!' }
    ]
  },
  {
    id: 2,
    temp_name: 'Template B',
    checks: [
      { id: 3, check_cell: 'A1', check_value: 'Hello!' },
      { id: 3, check_cell: 'D3', check_value: 'Duyet' }
    ]
  }
])

// Mock oilrigs
mock.onGet('/api/templates').reply(200, [
  { id: 1, temp_name: 'Template A' },
  { id: 2, temp_name: 'Template B' }
])

mock.onPost('/api/oilrigs').reply(config => {
  const newRig = JSON.parse(config.data)
  console.log('Received new oilrig:', newRig)
  return [200, { message: 'Oilrig created successfully' }]
})

// Mock template create
mock.onGet('/api/templates/full-create').reply( 200, [
  {
    "temp_name": "Template A",
    "checks": [
      { "check_cell": "B2", "check_value": "Daily Report" }
    ],
    "data_locations": [
      {
        "data_cell": "C3",
        "report_type": "daily",
        "resource_type": "oil",
        "data_type": "real"
      }
    ],
    "oilrig_ids": [1, 2]
  }
])


// Mock report
mock.onGet('/api/reports/view-all').reply( 200, [
  {
    "template_id": 2,
    "matched_template_name": "Monthly Template B",
    "real_oil": 3210.5,
    "real_gas": 9876.0,
    "planned_oil": 3210.5,
    "planned_gas": 9876.0,
    "report_date": "2025-03-20",
    "name": "Rig_11"
  },
  {
    "template_id": 3,
    "matched_template_name": "Monthly Template C",
    "real_oil": 13123,
    "real_gas": 2133,
    "planned_oil": 123,
    "planned_gas": 1123,
    "report_date": "2025-03-20",
    "name": "Rig_14"
  }
])
