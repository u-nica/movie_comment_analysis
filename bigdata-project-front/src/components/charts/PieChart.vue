<template>
  <div class="chart-wrapper">
    <h2>{{ year }}年全国油料产量分布</h2>
    <v-chart :option="option" autoresize v-if="hasData" />
    <div v-else class="no-data">暂无数据</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { EChartsOption } from 'echarts';

const props = defineProps<{
  data: { name: string; value: number }[];
  year: number;
}>();

// 检查是否有有效数据
const hasData = computed(() => {
  return props.data && props.data.length > 0 && props.data.some(item => item.value > 0);
});

const option = computed<EChartsOption>(() => {
  if (!hasData.value) return {};

  // 计算总量用于百分比显示
  const total = props.data.reduce((sum, item) => sum + item.value, 0);

  return {
    textStyle: { color: '#e0e0e0' },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const percent = total > 0 ? ((params.value / total) * 100).toFixed(1) : '0';
        return `${params.name}<br/>产量: ${params.value.toLocaleString()}吨 (${percent}%)`;
      }
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 'center',
      bottom: 20,
      formatter: (name: string) => {
        const item = props.data.find(d => d.name === name);
        if (item && total > 0) {
          const percent = ((item.value / total) * 100).toFixed(1);
          return `${name}: ${percent}%`;
        }
        return name;
      },
      textStyle: {
        color: '#e0e0e0'
      },
      pageTextStyle: {
        color: '#e0e0e0'
      },
      padding: [0, 0, 0, 20]
    },
    series: [
      {
        name: '油料产量',
        type: 'pie',
        radius: ['35%', '65%'],
        center: ['40%', '40%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#e0e0e0',
          borderWidth: 1
        },
        label: {
          show: true,
          formatter: (params: any) => {
            return `{b|${params.name}}\n{d|${params.percent}%}`;
          },
          rich: {
            b: { fontSize: 12, lineHeight: 20, color: '#e0e0e0' },
            d: { fontSize: 14, fontWeight: 'bold', color: '#e0e0e0' }
          },
          position: 'outside',
          padding: [0, -40]
        },
        labelLine: {
          show: true,
          length: 35,
          length2: 50,
          minTurnAngle: 60,
          showAbove: true
        },
        emphasis: {
          scale: true,
          scaleSize: 5
        },
        data: props.data
      }
    ],
    graphic: [
      {
        type: 'text',
        left: '35%',
        top: '38%',
        style: {
          text: total.toLocaleString() + '吨',
          textAlign: 'center',
          fill: '#e0e0e0',
          fontSize: 15,
          fontWeight: 'bold'
        }
      },
      {
        type: 'text',
        left: '35%',
        top: '43%',
        style: {
          text: '总产量',
          textAlign: 'center',
          fill: '#aaa',
          fontSize: 13
        }
      }
    ],
    color: ['#76b7b2', '#FAC858', '#91CC75', '#EE6666', '#73C0DE', '#9A60B4', '#3ba272', '#fc8452', '#ea7ccc']
  };
});
</script>

<style scoped>
.chart-wrapper {
  height: 100%;
  width: 95%;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  overflow: hidden;
  margin-bottom: 24px; 
}

.chart-wrapper:hover {
  transition: all 0.3s ease;
}

h2 {
  margin: 0; 
  margin-bottom: 20px;
  font-size: 20px;
  color: #e0e0e0;
  font-weight: 600; 
  letter-spacing: 0.5px; 
  text-align: center; 
}
.no-data {
  color: #999;
  font-size: 1.1em;
  margin-top: 50px;
}
</style>