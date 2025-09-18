console.log('main.ts: Checkpoint 1 - File loaded and script starts.');

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import * as echarts from 'echarts'  
import VChart from 'vue-echarts' 

import './assets/main.css' 

const app = createApp(App)

console.log('main.ts: Checkpoint 2 - App created.');

app.component('v-chart', VChart) 

app.config.globalProperties.$echarts = echarts 
app.use(createPinia())
app.use(router)
app.mount('#app')
console.log('main.ts: Checkpoint 3 - App mounted.');