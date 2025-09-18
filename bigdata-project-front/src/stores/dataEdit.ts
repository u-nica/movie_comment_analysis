import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getRawData, upsertData, deleteData, type RawData } from '../api';

export const useDataEditStore = defineStore('data-edit', () => {
  // --- State: 状态 ---
  const tableData = ref<RawData[]>([]); // 存储从后端获取的表格数据
  const isLoading = ref(false); // 控制加载动画的显示
  const error = ref<string | null>(null); // 存储错误信息

  // --- Actions: 行为 ---

  // 1. 获取原始数据
  async function fetchRawData(filters: { year?: number; province?: string }) {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await getRawData(filters);
      tableData.value = response.data;
      } catch (e: any) {
      error.value = '获取数据失败，请重试。';
      console.error(e);
      tableData.value = []; // 出错时清空数据
    } finally {
      isLoading.value = false;
    }
  }

  // 2. 更新或插入数据
  async function handleUpsert(data: RawData) {
    isLoading.value = true;
    try {
      await upsertData(data);
      // 操作成功后，可以弹窗提示用户
      alert('数据保存成功！');
      // 刷新当前页面的数据
      return true;
    } catch (e) {
      alert('数据保存失败！');
      console.error(e);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  // 3. 删除数据
  async function handleDelete(data: { year: number; province: string; city?: string; county?: string }) {
    isLoading.value = true;
    try {
      await deleteData(data);
      alert('数据删除成功！');
       // 刷新当前页面的数据
      return true;
    } catch (e) {
      alert('数据删除失败！');
      console.error(e);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    tableData,
    isLoading,
    error,
    fetchRawData,
    handleUpsert,
    handleDelete,
  };
});