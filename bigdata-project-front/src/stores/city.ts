import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getCityStats } from '../api';

// 定义城市数据类型
export interface CityData {
  city: string;
  total_yield_ton: number;
  percentage: number;
}

export const useCityStore = defineStore('city', () => {
  const cityStats = ref<CityData[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const dataMissing = ref(false);

  async function fetchCityStats(province: string, year: number) {
    isLoading.value = true;
    error.value = null;
    cityStats.value = []; 
    dataMissing.value = false;

    try {
      const response = await getCityStats(province, year);
      
      // 检查后端返回的数据缺失状态
      if (response.data.code === 404) {
        dataMissing.value = true;
        cityStats.value = [];
      } else {
        cityStats.value = response.data;
        dataMissing.value = false;
      }
    } catch (e: any) {
      error.value = `无法加载 ${province} 在 ${year} 年的城市数据。`;
      console.error(e);
      dataMissing.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    cityStats,
    isLoading,
    error,
    dataMissing,
    fetchCityStats
  };
});