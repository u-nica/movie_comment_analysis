<template>
  <div class="province-map-container">
    <v-chart v-if="!loading && mapJson" :option="option" autoresize />
    <div v-if="loading" class="status-message">地图加载中...</div>
    <div v-if="!loading && !mapJson" class="status-message">无法加载本地地图文件，请检查文件路径。</div>
    
    <div v-if="showDataMissing" class="data-missing-overlay">
      <div class="data-missing-text">数据缺失</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';

const props = defineProps<{
  provinceName: string; 
  data: { name: string; value: number }[]; // 城市数据, e.g., [{ name: '哈尔滨市', value: 12345.6 }]
}>();

const mapJson = ref<any>(null); 
const loading = ref(true); 

//根据省份名称生成地图文件名
const mapFileName = computed(() => props.provinceName);

// 检查是否有数据缺失
const showDataMissing = computed(() => {
  // 当数据数组为空或所有值都是0时显示数据缺失提示
  return props.data.length === 0 || props.data.every(item => item.value === 0);
});

// 异步加载地图数据
async function loadMapData() {
  if (!mapFileName.value) { 
    loading.value = false;
    mapJson.value = null;
    return;
  }
  
  loading.value = true;
  mapJson.value = null; 
  try {
    // 尝试加载指定省份的 GeoJSON 文件
    const response = await axios.get(`/maps/provinces/${mapFileName.value}.json`);
    mapJson.value = response.data;
  } catch (error) {
    // 加载失败时打印错误信息并设置 mapJson 为 null
    console.error(`加载 ${props.provinceName} 的地图文件失败:`, error);
    mapJson.value = null;
  } finally {
    loading.value = false;
  }
}

onMounted(loadMapData); // 组件挂载时加载地图数据
watch(() => props.provinceName, loadMapData); // 监听省份名称变化，重新加载地图数据

const option = computed(() => {
  // 如果正在加载或地图数据不存在，则返回空对象
  if (loading.value || !mapJson.value) return {};

  // 注册地图数据
  // @ts-ignore
  echarts.registerMap(mapFileName.value, mapJson.value); 

  // 计算最大值，如果数据缺失则使用默认值
  const maxValue = showDataMissing.value 
    ? 1000 
    : Math.max(...props.data.map(d => d.value), 1000); 

  return {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `${params.name}<br/>产量: ${params.value} (吨)`;
      },
      textStyle: { color: '#333333' }
    },
    visualMap: {
      min: 0,
      max: maxValue,
      left: 'left',
      bottom: 'bottom',
      text: ['高', '低'],
      calculable: true,
      inRange: {
        color: showDataMissing.value 
          ? ['#cccccc'] 
          : ['#BEE5FD', '#0052D9'] 
      },
      textStyle: {
        color: '#e0e0e0' 
      }
    },
    series: [
      {
        name: `${props.provinceName} 油料产量`,
        type: 'map',
        map: mapFileName.value,
        roam: true,
        data: showDataMissing.value 
          ? [] 
          : props.data.map(item => ({
              ...item,
              value: item.value === 0 ? -1 : item.value
            })),
        itemStyle: {
          areaColor: '#fff', 
          borderColor: '#333333', 
          borderWidth: 0.5 
        },
        emphasis: {
            label: { show: true, color: '#e0e0e0' },
            itemStyle: { areaColor: '#ffc107' }
        },
      },
    ],
    textStyle: {
      color: '#e0e0e0' 
    }
  };
});
</script>

<style scoped>
.province-map-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.status-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 1.2em;
  color: #e0e0e0; 
}
</style>