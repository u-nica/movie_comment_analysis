<template>
  <div class="home-view">
    <div class="page-header">
      <div class="header-content">
        <h1>
          2000-2020年全国油料产量分析及预测系统
        </h1>
        <div class="header-actions">
          <button 
            class="action-btn primary"
            @click="refreshData"
            :disabled="statsStore.isLoading">
            刷新数据
          </button>
          
          <div class="province-selector">
            <select v-model="selectedProvince">
              <option v-for="province in provinceList" :key="province" :value="province">
                {{ province }}
              </option>
            </select>
          </div>
          
          <button 
            class="action-btn info"
            @click="goToProvinceDetail">
            查看省份详情
          </button>
          
          <button 
            class="action-btn success"
            @click="goToDataEditPage">
            修改数据
          </button>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div v-if="statsStore.isLoading" class="loading">正在加载数据...</div>
      <div v-if="statsStore.error" class="error">{{ statsStore.error }}</div>

      <div v-if="!statsStore.isLoading && !statsStore.error">
        <div class="stats-section">
          <div class="stats-grid">
            <div 
              v-for="stat in statsCards" 
              :key="stat.key"
              class="stat-card"
              :class="stat.type">
              <div class="stat-content">
                <div class="stat-icon">
                  {{ stat.icon }}
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="charts-section">
          <div class="chart-row">
            <div class="map-container chart-item">
              <ChinaMap 
                :data="mapData" 
                @province-click="handleProvinceClick"
              />
            </div>
            <div class="pie-container chart-item">
              <PieChart :data="pieData" :year="selectedYear" />
            </div>
          </div>

          <div class="slider-container">
            <span>年份选择：</span>
            <input type="range" min="2000" max="2020" v-model.number="selectedYear" />
            <span class="year-label">{{ selectedYear }}</span>
          </div>

          <div class="chart-item">
            <div class="prediction-card">
              <PredictionLineChart />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStatsStore } from '../stores/stats';
import ChinaMap from '../components/ChinaMap.vue';
import PieChart from '../components/charts/PieChart.vue';
import PredictionLineChart from '../components/charts/prediction.vue';

const router = useRouter();
const statsStore = useStatsStore();
const selectedYear = ref(2020);
const selectedProvince = ref('陕西省');

onMounted(() => {
  statsStore.fetchAllStats();
});

// 获取省份列表
const provinceList = computed(() => {
  return Object.keys(statsStore.allStats);
});

// 统计卡片数据
const statsCards = computed(() => {
  const totalProduction = mapData.value.reduce((sum, item) => sum + item.value, 0);
  const provinceCount = mapData.value.length;
  const avgProduction = provinceCount > 0 ? Math.round(totalProduction / provinceCount) : 0;
  
  // 找到最高产量的省份
  const topProvince = mapData.value.length 
    ? [...mapData.value].sort((a, b) => b.value - a.value)[0] 
    : null;

  return [
    {
      key: 'total-production',
      label: '全国总产量',
      value: totalProduction.toLocaleString() + ' 吨',
      icon: '📊',
      type: 'primary'
    },
    {
      key: 'avg-production',
      label: '省份平均产量',
      value: avgProduction.toLocaleString() + ' 吨',
      icon: '⚖️',
      type: 'success'
    },
    {
      key: 'top-province',
      label: topProvince ? `${topProvince.name}产量` : '最高产省份',
      value: topProvince ? topProvince.value.toLocaleString() + ' 吨' : 'N/A',
      icon: '🏆',
      type: 'warning'
    },
    {
      key: 'year',
      label: '当前选择年份',
      value: selectedYear.value,
      icon: '📅',
      type: 'info'
    }
  ];
});

const mapData = computed(() => {
  const data = [];
  const stats = statsStore.allStats;
  for (const province in stats) {
    const yearData = stats[province].find(d => d.year === selectedYear.value);
    if (yearData) {
      data.push({ name: province, value: yearData.production });
    }
  }
  return data;
});

const pieData = computed(() => {
  const allData = [...mapData.value];
  if (allData.length === 0) return [];
  const totalValue = allData.reduce((sum, item) => sum + item.value, 0);
  const top5 = [...allData]
    .sort((a, b) => b.value - a.value)
    .slice(0, 5);
  const otherValue = totalValue - top5.reduce((sum, item) => sum + item.value, 0);
  const result = top5.map(item => ({ 
    name: item.name, 
    value: item.value 
  }));
  if (otherValue > 0) {
    result.push({ 
      name: '其他省份', 
      value: otherValue 
    });
  }
  
  return result;
});

const handleProvinceClick = (provinceName: string) => {
  selectedProvince.value = provinceName;
  goToProvinceDetail();
};

// 刷新数据 - 增强刷新逻辑
const refreshData = () => {
  // 显示加载状态
  statsStore.isLoading = true;
    // 重置年份选择
  selectedYear.value = 2020;
    // 强制刷新数据
  statsStore.fetchAllStats().finally(() => {
    // 添加一点延迟让用户感知到刷新
    setTimeout(() => {
      statsStore.isLoading = false;
    }, 500);
  });
};

// 跳转到数据编辑页面
const goToDataEditPage = () => {
  router.push({ name: 'data-edit' });
};

// 查看省份详情
const goToProvinceDetail = () => {
  router.push({ 
    name: 'province', 
    params: { name: selectedProvince.value },
    query: { year: selectedYear.value }
  });
};
</script>

<style scoped>
.home-view {
  background-color: #85afd1; 
  min-height: 100vh;
  padding-bottom: 20px;
}

.page-header {
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%); 
  color: white;
  padding: 0 24px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 0;
  max-width: 1400px;
  margin: 0 auto;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #e0e0e0; 
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #e0e0e0;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary {
  background-color: #a28923; 
  color: rgb(255, 255, 255);
}

.success {
  background-color: #8bd89f; 
  color: white;
}

.info {
  background-color: #57afa8; 
  color: white;
}

.province-selector {
  position: relative;
}

.province-selector select {
  padding: 10px 16px;
  padding-right: 40px;
  border: 1px solid rgba(255, 255, 255, 0.3); 
  border-radius: 6px;
  background-color: #2f4362; 
  font-size: 14px;
  color: #e0e0e0; 
  appearance: none;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 140px;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23e0e0e0' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
}

.province-selector select:focus {
  border-color: #0052D9;
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 82, 217, 0.2);
}

.main-content {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.stats-section {
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%); 
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  padding: 16px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3); 
  border-left: 4px solid;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); 
}

.stat-card.primary {
  border-left-color: #d55f5f; 
}

.stat-card.success {
  border-left-color: #00cf45ff;
}

.stat-card.warning {
  border-left-color: #FAC858; 
}

.stat-card.info {
  border-left-color: #76b7b2; 
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 28px;
  color: #e0e0e0;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #e0e0e0; 
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.charts-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
  gap: 20px;
}

.chart-item {
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.chart-item:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); 
  transform: translateY(-5px);
}

.map-container, .pie-container {
  height: 500px;
  background-color: transparent; 
}

.slider-container {
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%); 
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); 
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.slider-container:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); 
  transform: translateY(-5px);
}

.slider-container span {
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

.prediction-card {
  background-color: transparent;
  border-radius: 12px;
  padding: 20px;
  height: 450px;
}

@media (max-width: 1200px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .map-container, .pie-container {
    height: 450px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .header-actions {
    width: 100%;
    flex-direction: column;
    gap: 10px;
  }
  
  .province-selector {
    width: 100%;
  }
  
  .province-selector select {
    width: 100%;
    min-width: auto;
  }
  
  .action-btn {
    width: 100%;
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .map-container, .pie-container, .prediction-card {
    height: 350px;
  }
  
  input[type="range"] {
    width: 70%;
  }
  
  .main-content {
    padding: 16px;
  }
}
</style>