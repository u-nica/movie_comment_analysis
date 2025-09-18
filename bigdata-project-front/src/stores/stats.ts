import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getAllProvinceStats } from '../api' 

export interface YearData {
  year: number;
  production: number;
  growth_rate: number;
}

export interface ProvinceStats {
  [provinceName: string]: YearData[];
}

export const useStatsStore = defineStore('stats', () => {
  // State: 存储所有省份的数据
  const allStats = ref<ProvinceStats>({});
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Action: 异步获取数据
  async function fetchAllStats() {
    if (Object.keys(allStats.value).length > 0) {
      // 如果已经有数据，就不再重复获取
      return;
    }
    isLoading.value = true;
    error.value = null;
    try {
      const response = await getAllProvinceStats();
      allStats.value = response.data; 
    } catch (e) {
      error.value = '数据加载失败，请稍后重试。';
      console.error(e);
    } finally {
      isLoading.value = false;
    }
  }

  return {
    allStats,
    isLoading,
    error,
    fetchAllStats
  }
})