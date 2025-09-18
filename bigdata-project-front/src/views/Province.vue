<template>
  <div class="province-view">
    <div class="header">
      <h1 class="title">{{ name }} 油料产量分析</h1>
      <button @click="router.back()" class="back-button">返回主页</button>
    </div>

    <!-- 简化状态提示 -->
    <div v-if="cityStore.isLoading" class="status-message">正在加载 {{ currentYear }} 年的数据...</div>
    <div v-else-if="cityStore.error" class="status-message error">{{ cityStore.error }}</div>
    <div v-else-if="cityStore.dataMissing" class="full-missing-overlay">
      <div class="missing-data-text">⚠️ {{ name }} {{ currentYear }} 年的数据缺失</div>
    </div>

    <div v-else class="content-grid">
      <div class="top-section">
        <div class="map-container chart-item">
          <ProvinceMap :province-name="name" :data="cityMapData" />
        </div>
        <div class="pie-container chart-item">
          <CityDistributionChart :data="cityStore.cityStats" :year="currentYear" />
        </div>
      </div>
      
      <div class="year-slider-container">
          <span>年份选择：</span>
          <input type="range" min="2000" max="2020" v-model.number="currentYear" />
          <span class="year-label">{{ currentYear }}</span>
      </div>

      <div class="bottom-section">
        <div class="chart-row">
          <div class="chart-card chart-item">
            <h2>历年产量趋势</h2>
            <div v-if="provinceDataMissing" class="missing-data-overlay">
              <div class="missing-data-text">数据缺失</div>
            </div>
            <v-chart v-else :option="productionOption" autoresize />
          </div>
          <div class="chart-card chart-item">
            <h2>历年产量增长率</h2>
            <div v-if="provinceDataMissing" class="missing-data-overlay">
              <div class="missing-data-text">数据缺失</div>
            </div>
            <v-chart v-else :option="growthOption" autoresize />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStatsStore } from '../stores/stats';
import { useCityStore } from '../stores/city';
import type { EChartsOption } from 'echarts';

import ProvinceMap from '../components/ProvinceMap.vue';
import CityDistributionChart from '../components/charts/CityPieChart.vue';

const route = useRoute();
const router = useRouter();
const props = defineProps<{ name: string }>();
const statsStore = useStatsStore();
const cityStore = useCityStore();

const initialYear = Number(route.query.year) || 2020;
const currentYear = ref(initialYear);

const provinceDataMissing = computed(() => {
  const key = `${props.name}`;
  return !statsStore.allStats[key] || statsStore.allStats[key].length === 0;
});

onMounted(() => {
  statsStore.fetchAllStats(); 
  cityStore.fetchCityStats(props.name, currentYear.value);
});

watch(currentYear, (newYear) => {
  cityStore.fetchCityStats(props.name, newYear);
  router.replace({ query: { year: newYear } });
});

const cityMapData = computed(() => {
  return cityStore.cityStats.map(d => ({
    name: d.city,
    value: d.total_yield_ton, 
  }));
});

const provinceAllYearsData = computed(() => {
  const key = `${props.name}`;
  return statsStore.allStats[key] || [];
});

const productionOption = computed<EChartsOption>(() => {
  const data = provinceAllYearsData.value;
  if (!data || data.length === 0) return {};
  
  const sortedData = [...data].sort((a, b) => a.year - b.year);
  
  return {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: sortedData.map(d => d.year),
      axisLabel: { color: '#e0e0e0' }
    },
    yAxis: { 
      type: 'value', 
      name: '吨',
      nameTextStyle: { color: '#e0e0e0' },
      axisLabel: { color: '#e0e0e0' }
    },
    series: [{
      data: sortedData.map(d => d.production),
      type: 'line',
      smooth: true,
      itemStyle: { color: '#73C0DE' }
    }],
    grid: { left: '15%', right: '5%', bottom: '10%' },
    textStyle: { color: '#e0e0e0' } 
  };
});

const growthOption = computed<EChartsOption>(() => {
  const data = provinceAllYearsData.value;
  if (!data || data.length === 0) return {};
  
  return {
    tooltip: { 
      trigger: 'axis',
      formatter: '{b}年<br/>增长率: {c}%'
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.year),
      axisLabel: { color: '#e0e0e0' } /* 添加文本颜色 */
    },
    yAxis: { 
      type: 'value',
      axisLabel: { formatter: '{value} %', color: '#e0e0e0' } /* 添加文本颜色 */
    },
    series: [{
      data: data.map(d => parseFloat((d.growth_rate * 100).toFixed(2))),
      type: 'bar',
      itemStyle: { color: '#91CC75' } /* 调整柱状图颜色 */
    }],
    grid: { left: '15%', right: '5%', bottom: '10%' },
    textStyle: { color: '#e0e0e0' } /* 添加文本颜色以保持整体一致性 */
  };
});
</script>

<style scoped>
/* 新增全屏覆盖层样式 */
.full-missing-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.3);
  margin-top: 20px;
}

.full-missing-overlay .missing-data-text {
  font-size: 2.5em;
  font-weight: bold;
  color: #EE6666;
  padding: 40px 60px;
  border: 3px dashed #EE6666;
  border-radius: 10px;
  background-color: rgba(47, 67, 98, 0.9);
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}


.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #e0e0e0;
}

.province-view {
  padding: 20px;
  background-color: #85afd1;
  min-height: 100vh;
}

.title {
  font-size: 2.2em;
  color: #e0e0e0; 
}
.back-button {
  padding: 10px 16px;
  background-color: #0052D9;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px; 
  transition: all 0.3s ease;
}
.back-button:hover {
  background-color: #007bff; 
}

.status-message {
  text-align: center;
  font-size: 1.5em;
  color: #e0e0e0;
  padding: 50px;
}
.error {
  color: #EE6666;
}
.content-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.top-section {
  display: grid;
  grid-template-columns: 1fr 1fr; 
  gap: 20px;
  margin-bottom: 30px;
}

.bottom-section {
  margin-top: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr; 
  gap: 20px;
}

.map-container, 
.pie-container,
.chart-card { 
  min-height: 500px;
  min-width: 500px;
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%); 
  border-radius: 16px;
  padding: 24px; 
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.chart-item:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  transform: translateY(-5px);
}

.chart-card h2 {
  margin: 0; 
  margin-bottom: 20px;
  font-size: 20px; 
  color: #e0e0e0; 
  font-weight: 600; 
  letter-spacing: 0.5px; 
  text-align: center; 
}

.year-slider-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  padding: 20px; 
  border-radius: 16px; 
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); 
  margin: 10px 0;
  border: 1px solid rgba(255, 255, 255, 0.3); 
  transition: all 0.3s ease;
}

.year-slider-container:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); 
  transform: translateY(-5px);
}

.year-slider-container span {
  font-size: 16px;
  color: #e0e0e0;
  margin: 0 10px;
}

input[type="range"] {
  width: 400px; 
  height: 6px;
  border-radius: 3px;
  background: #4a5a70;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #0052D9;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  margin-top: -6px; 
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #0052D9; 
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.year-label {
  font-weight: bold;
  font-size: 18px;
  min-width: 50px;
  color: #e0e0e0;
}

.missing-data-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(26, 42, 67, 0.8); 
  z-index: 5;
  border-radius: 16px;
}

.missing-data-text {
  font-size: 2.5em;
  font-weight: bold;
  color: #EE6666;
  padding: 20px 40px;
  border: 3px dashed #EE6666;
  border-radius: 10px;
  background-color: rgba(47, 67, 98, 0.9);
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@media (max-width: 1200px) {
  .top-section, .chart-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 1.8em;
  }
  .back-button {
    padding: 8px 12px;
    font-size: 0.9em;
  }
  .map-container, .pie-container, .chart-card {
    min-height: 350px;
    min-width: auto;
  }
  .year-slider-container {
    flex-direction: column;
    gap: 10px;
  }
  input[type="range"] {
    width: 90%;
  }
  .missing-data-text {
    font-size: 1.8em;
    padding: 15px 30px;
  }
}
</style>