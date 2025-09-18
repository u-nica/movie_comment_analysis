<template>
  <div class="chart-wrapper">
    <h2>{{ year }} 年各市产量占比</h2>
    <v-chart :option="option" autoresize v-if="hasData" />
    <div v-else class="no-data">暂无数据</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { EChartsOption } from 'echarts'; 

interface ChartData {
  city: string;
  total_yield_ton: number;
}

interface ProcessedData {
  city: string;
  total_yield_ton: number;
}

const props = defineProps<{
  data: ChartData[];
  year: number;
}>();

const hasData = computed(() => {
  return props.data && props.data.length > 0 && props.data.some(item => item.total_yield_ton > 0);
});

const option = computed<EChartsOption>(() => {
  if (!hasData.value) return {}; 

  // 合并小扇区（小于总产量2%的合并为"其他"）
  const threshold = 0.02;
  let otherTotal = 0;
  const mainData: ProcessedData[] = []; 
  
  const sortedData = [...props.data].sort((a, b) => b.total_yield_ton - a.total_yield_ton);
  const total = sortedData.reduce((sum, item) => sum + item.total_yield_ton, 0);

  sortedData.forEach(item => {
    const percentage = item.total_yield_ton / total;
    if (percentage < threshold) {
      otherTotal += item.total_yield_ton;
    } else {
      mainData.push({
        city: item.city,
        total_yield_ton: item.total_yield_ton
      });
    }
  });

  if (otherTotal > 0) {
    mainData.push({
      city: "其他",
      total_yield_ton: otherTotal
    });
  }

  const pieData = mainData.map(item => ({
    name: item.city,
    value: item.total_yield_ton
  }));

  // 只显示前8名的标签
  const showLabelData = pieData.slice(0, 8);
  const hideLabelData = pieData.slice(8);

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
        const item = mainData.find(d => d.city === name);
        if (item && total > 0) {
          const percent = ((item.total_yield_ton / total) * 100).toFixed(1);
          return `${name}: ${percent}%`;
        }
        return name;
      },
      textStyle: { color: '#e0e0e0' },
      pageTextStyle: { color: '#e0e0e0' },
      padding: [0, 0, 0, 20]
    },
    series: [
      {
        name: '城市产量',
        type: 'pie',
        radius: ['35%', '65%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#e0e0e0',
          borderWidth: 1
        },
        label: {
          show: true,
          formatter: (params: any) => {
            // 只显示前8名的详细标签
            if (params.dataIndex < 8) {
              return `{b|${params.name}}\n{d|${params.percent}%}`;
            }
            return '';
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
          length: 80,
          length2: 50,
          minTurnAngle: 60,
          showAbove: true
        },
        emphasis: {
          scale: true,
          scaleSize: 5
        },
        data: [
          ...showLabelData.map(item => ({
            ...item,
            label: { show: true }
          })),
          ...hideLabelData.map(item => ({
            ...item,
            label: { show: false },
            labelLine: { show: false }
          }))
        ]
      }
    ],
    graphic: [
      {
        type: 'text',
        left: '35%',
        top: '45%',
        style: {
          text: total.toLocaleString() + '吨',
          textAlign: 'center',
          fill: '#e0e0e0',
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      {
        type: 'text',
        left: '35%',
        top: '52%',
        style: {
          text: '总产量',
          textAlign: 'center',
          fill: '#aaa',
          fontSize: 12
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