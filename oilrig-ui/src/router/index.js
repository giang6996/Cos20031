import { createRouter, createWebHistory } from 'vue-router'

import Oilrigs from '../pages/Oilrigs.vue'
import OilrigCreate from '../pages/OilrigCreate.vue'
import Templates from '../pages/Templates.vue'
import TemplateCreate from '../pages/TemplateCreate.vue'
import Reports from '../pages/Reports.vue'
import ReportDaily from '../pages/ReportDaily.vue'
import ReportMonthly from '../pages/ReportMonthly.vue'
import ReportUpload from '../pages/ReportUpload.vue'
import ReportWeekly from '../pages/ReportWeekly.vue'
import ReportQuarterly from '../pages/ReportQuarterly.vue'
import ReportAnnually from '../pages/ReportAnnually.vue'
import ReportDailyPercent from '../pages/ReportDailyPercent.vue'
import ReportMonthlyPercent from '../pages/ReportMonthlyPercent.vue'
import ReportMonthlyAnnuallyPercent from '../pages/ReportMonthlyAnnuallyPercent.vue'
import ReportYearly from '../pages/ReportYearly.vue'
import ReportDailyRigName from '../pages/ReportDailyRigName.vue'
import ReportCombine from '../pages/ReportCombine.vue'



const routes = [
    {path: '/', component: ReportDaily},
    {path: '/Oilrigs', component: Oilrigs},
    {path: '/Oilrigs/Create', component: OilrigCreate},
    {path: '/Templates', component: Templates},
    {path: '/Templates/Create', component: TemplateCreate},
    {path: '/Reports', component: Reports},
    {path: '/Reports/All', component: ReportCombine},
    {path: '/Reports/Daily-rig-name', component: ReportDailyRigName},
    {path: '/Reports/Daily', component: ReportDaily},
    {path: '/Reports/Upload', component: ReportUpload},
    {path: '/Reports/Monthly', component: ReportMonthly},
    {path: '/Reports/Weekly', component: ReportWeekly},
    {path: '/Reports/Quarterly', component: ReportQuarterly},
    {path: '/Reports/Annually', component: ReportAnnually},
    {path: '/Reports/Percent-daily', component: ReportDailyPercent},
    {path: '/Reports/Percent-monthly', component:ReportMonthlyPercent},
    {path: '/Reports/Percent-monthly-annually', component:ReportMonthlyAnnuallyPercent},
    {path: '/Reports/Percent-yearly', component: ReportYearly}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router