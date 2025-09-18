<template>
  <div class="chart-wrapper">
    <h2>全国油料产量趋势及预测 (吨)</h2>
    <v-chart :option="option" autoresize v-if="hasData" />
    <div v-else class="no-data">
      正在加载预测数据或暂无数据...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useStatsStore } from '../../stores/stats';
import { getNationalPrediction } from '../../api';

const statsStore = useStatsStore();

const chartData = ref<{ year: number; production: number }[]>([]);
const predictedData = ref<{ year: number; production: number }[]>([]);

const fetchPredictionData = async () => {
    try {
        const response = await getNationalPrediction();
        if (response.data && response.data) {
            predictedData.value = response.data.map((item: { year: number; prediction: number }) => ({
                year: item.year,
                production: item.prediction
            }));
        }
    } catch (error) {
        console.error('Error fetching prediction data:', error);
    }
};

const nationalProductionByYear = computed(() => {
  const yearsMap: { [year: number]: number } = {};
  for (const province in statsStore.allStats) {
    statsStore.allStats[province].forEach(data => {
      if (!yearsMap[data.year]) {
        yearsMap[data.year] = 0;
      }
      yearsMap[data.year] += data.production;
    });
  }
  return Object.keys(yearsMap).map(year => ({
    year: parseInt(year),
    production: yearsMap[parseInt(year)]
  })).sort((a, b) => a.year - b.year);
});

watch(nationalProductionByYear, (newValue) => {
    chartData.value = newValue;
    if (newValue.length > 0) {
        fetchPredictionData();
    }
}, { immediate: true });

const hasData = computed(() => chartData.value.length > 0 || predictedData.value.length > 0);

const option = computed(() => {
  const years = chartData.value.map(d => d.year);
  const predictedYears = predictedData.value.map(d => d.year);
  const lastHistoricalYear = years.length > 0 ? years[years.length - 1] : null;

  const allYears = Array.from(new Set([...years, ...predictedYears])).sort((a,b) => a - b);

  const actualProductionData = allYears.map(year => {
    const dataPoint = chartData.value.find(d => d.year === year);
    return dataPoint ? dataPoint.production : null;
  });

  const predictedProductionDataFormatted = allYears.map(year => {
    const historicalDataPoint = chartData.value.find(d => d.year === year);
    const predictionDataPoint = predictedData.value.find(d => d.year === year);

    if (lastHistoricalYear !== null) {
      if (year < lastHistoricalYear) {
        return null; 
      } else if (year === lastHistoricalYear) {
        return historicalDataPoint ? historicalDataPoint.production : null;
      } else if (year > lastHistoricalYear && predictionDataPoint) {
        return predictionDataPoint.production;
      }
    }
    return null;
  });

  return {
    tooltip: {
      trigger: 'axis',
      formatter: function (params: any[]) {
        if (!params || params.length === 0) {
          return '';
        }

        const year = parseInt(params[0].name);
        let res = year + '年<br/>';

        const actualSeriesItem = params.find(item => item.seriesName === '实际产量');
        const predictedSeriesItem = params.find(item => item.seriesName === '预测产量');

        if (lastHistoricalYear !== null && year <= lastHistoricalYear && actualSeriesItem && actualSeriesItem.value !== null) {
            res += actualSeriesItem.marker + '实际产量: ' + actualSeriesItem.value + ' (吨)<br/>';
        } else if (lastHistoricalYear !== null && year > lastHistoricalYear && predictedSeriesItem && predictedSeriesItem.value !== null) {
            res += predictedSeriesItem.marker + '预测产量: ' + predictedSeriesItem.value + ' (吨)<br/>';
        }

        return res;
      },
    },
    legend: {
      data: ['实际产量', '预测产量'],
      bottom: 0,
      selected: {
        '实际产量': true,
        '预测产量': true
      },
      textStyle: {
      color: '#e0e0e0' 
    },
    },
    xAxis: {
      type: 'category',
      data: allYears,
      axisLabel: {
        formatter: '{value}年'
      }
    },
    yAxis: {
      type: 'value',
      name: '吨'
    },
    textStyle: {
    color: '#e0e0e0' 
    },
    series: [
      {
        name: '实际产量',
        type: 'line',
        smooth: true,
        data: actualProductionData,
        itemStyle: {
            color: '#a2d5f2'
        },
        markLine: {
          silent: true,
          data: [
            {
              xAxis: lastHistoricalYear, 
              lineStyle: {
                type: 'dashed',
                color: '#000',
                width: 2
              },
              label: {
                formatter: '预测开始'
              }
            }
          ]
        }
      },
      {
        name: '预测产量',
        type: 'line',
        smooth: true,
        data: predictedProductionDataFormatted, 
        lineStyle: {
          type: 'dashed',
          color: '#EE6666'
        },
        itemStyle: {
            color: '#EE6666'
        },
      }
    ]
  };
});
</script>

<style scoped>
.chart-wrapper {
  height: 100%;
  width: 1500;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
h2 {
  margin-top: 0;
  font-size: 1.2em;
  color: #e0e0e0;
}
.no-data {
  color: #999;
  font-size: 1.1em;
}
</style>