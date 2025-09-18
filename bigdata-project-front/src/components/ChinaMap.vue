<template>
  <div class="map-container">
    <v-chart v-if="!loading" :option="option" autoresize @click="handleClick" />
    <div v-else class="status-message">地图加载中...</div> <div v-if="showDataMissing" class="data-missing-overlay">
      <div class="data-missing-text">数据缺失</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import type { EChartsOption } from 'echarts';
import axios from 'axios';
import * as echarts from 'echarts'; 

const props = defineProps<{
  data: { name: string; value: number }[];
}>();
const emit = defineEmits(['province-click']);

const chinaJson = ref(null);
const loading = ref(true);

// 计算属性：检查是否有数据缺失
const showDataMissing = computed(() => {
  // 当数据数组为空或所有值都是0时显示数据缺失提示
  return props.data.length === 0 || props.data.every(item => item.value === 0);
});

// 在组件挂载时异步加载 GeoJSON 文件
onMounted(async () => {
  try {
    const { data } = await axios.get('/maps/china.json');
    chinaJson.value = data;
  } catch (error) {
    console.error('加载地图数据失败:', error);
  } finally {
    loading.value = false;
  }
});

const option = computed<EChartsOption>(() => {
  if (loading.value || !chinaJson.value) return {};
  
  // 注册地图
  // @ts-ignore
  echarts.registerMap('china', chinaJson.value);

  // 计算最大值，如果数据缺失则使用默认值
  const maxValue = showDataMissing.value 
    ? 1000 
    : Math.max(...props.data.map(d => d.value), 1000);

  return {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        // 如果值为0或数据缺失（-1），显示"数据缺失"
        if (params.value === 0 || params.value === -1) {
          return `${params.name}<br/><span style="color: red;">数据缺失</span>`;
        }
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
          ? ['#cccccc'] // 数据缺失时使用灰色
          : ['#BEE5FD', '#0052D9'] 
      },
      textStyle: {
        color: '#e0e0e0'
      }
    },
    series: [
      {
        name: '油料产量',
        type: 'map',
        map: 'china',
        roam: true,
        itemStyle: {
          color: {
            type: 'linear', 
            x: 0,
            y: 0, 
            x2: 0,
            y2: 1,
            colorStops:[
              { offset: 0, color: '#2f4362' },
              { offset: 1, color: '#1a2a43' } 
            ]
          },
          opacity: 1,
          borderWidth: .5,
          borderColor: "#333333",
          fontSize: .1, 
        },
        data: showDataMissing.value 
          ? [] 
          : props.data.map(item => ({
              ...item,
              value: item.value === 0 ? -1 : item.value
            })),
        emphasis: {
            label: { show: true, color: '#000' }, 
            itemStyle: { areaColor: '#ffc107' }
        },
        viewControl: {
          distance: 120,
          alpha: 70, 
          beta: 0,
        },
      },
    ],
    textStyle: {
      color: '#333333' /* Added text color for general consistency */
    }
  };
});

const handleClick = (params: any) => {
  if (params.name) {
    emit('province-click', params.name);
  }
};
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%); /* Darker gradient for container */
  border-radius: 16px; /* Consistent border radius */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); /* Consistent shadow */
  border: 1px solid rgba(99, 98, 98, 0.3); /* Consistent border */
  overflow: hidden; /* Ensure content stays within bounds */
}

/* Status message style (for loading) */
.status-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 1.2em;
  color: #464646; /* Lighter text color */
}

/* 数据缺失提示样式 */
.data-missing-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(26, 42, 67, 0.8); /* Darker overlay */
  z-index: 10;
  border-radius: 16px; /* Match container border-radius */
}

.data-missing-text {
  font-size: 2.5em;
  font-weight: bold;
  color: #EE6666; /* Adjusted color */
  padding: 20px 40px;
  border: 3px dashed #EE6666; /* Adjusted color */
  border-radius: 10px;
  background-color: rgba(47, 67, 98, 0.9); /* Darker background for text */
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>