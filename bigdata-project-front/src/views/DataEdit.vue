<template>
  <div class="data-edit-view">
    <header class="header">
      <h1>数据管理中心</h1>
      <button @click="goBack" class="action-btn back">返回主页</button>
    </header>

    <div class="filters">
      <!-- 年份选择器 -->
      <div class="year-selector">
        <select v-model.number="filters.year">
          <option v-for="year in yearOptions" :key="year" :value="year">
            {{ year }}年
          </option>
        </select>
      </div>
      
      <!-- 省份选择器 -->
      <div class="province-selector">
        <select v-model="filters.province">
          <option value="">所有省份</option>
          <option v-for="province in provinceList" :key="province" :value="province">
            {{ province }}
          </option>
        </select>
      </div>
      
      <button @click="handleSearch" class="action-btn primary">查询</button>
      <button @click="openForm(null)" class="action-btn success">新增数据</button>
    </div>

    <div v-if="dataEditStore.isLoading" class="loading">正在加载...</div>
    <div v-if="dataEditStore.error" class="error">{{ dataEditStore.error }}</div>

    <div class="table-container" v-if="!dataEditStore.isLoading">
      <table>
        <thead>
          <tr>
            <th>年份</th>
            <th>省份</th>
            <th>城市</th>
            <th>县/区</th>
            <th>产量 (吨)</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="dataEditStore.tableData.length === 0">
            <td colspan="6" class="no-data">没有找到数据，请修改筛选条件或新增数据。</td>
          </tr>
          <tr v-for="item in dataEditStore.tableData" :key="`${item.province}-${item.year}-${item.city}`">
            <td>{{ item.year }}</td>
            <td>{{ item.province }}</td>
            <td>{{ item.city || '-' }}</td>
            <td>{{ item.county || '-' }}</td>
            <td>{{ item.yield }}</td>
            <td class="actions">
              <button @click="openForm(item)" class="action-btn info">编辑</button>
              <button @click="confirmDelete(item)" class="action-btn danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isFormVisible" class="modal-overlay" @click.self="closeForm">
      <div class="modal-content">
        <h2>{{ isEditing ? '编辑数据' : '新增数据' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>年份:</label>
            <input type="number" v-model="formData.year" required :disabled="isEditing" />
          </div>
          <div class="form-group">
            <label>省份:</label>
            <input type="text" v-model="formData.province" required :disabled="isEditing" />
          </div>
          <div class="form-group">
            <label>城市 (选填):</label>
            <input type="text" v-model="formData.city" :disabled="isEditing" />
          </div>
           <div class="form-group">
            <label>县/区 (选填):</label>
            <input type="text" v-model="formData.county" :disabled="isEditing" />
          </div>
          <div class="form-group">
            <label>产量 (吨):</label>
            <input type="number" v-model="formData.yield" required />
          </div>
          <div class="form-actions">
            <button type="button" @click="closeForm" class="action-btn esc">取消</button>
            <button type="submit" class="action-btn success">保存</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useDataEditStore } from '../stores/dataEdit'
import { useStatsStore } from '../stores/stats'; // 引入 stats store
import type { RawData } from '../api';

const router = useRouter();
const dataEditStore = useDataEditStore();
const statsStore = useStatsStore(); // 使用 stats store

// --- 筛选逻辑 ---
const filters = reactive({
  year: 2020,
  province: '',
});

// 年份选项 (2000-2020)
const yearOptions = Array.from({ length: 21 }, (_, i) => 2000 + i);

// 从 stats store 获取省份列表
const provinceList = computed(() => {
  // 确保 statsStore.allStats 已经加载
  if (Object.keys(statsStore.allStats).length === 0) {
    return [];
  }
  
  // 从 statsStore 的 allStats 中提取省份名称
  return Object.keys(statsStore.allStats).sort();
});

function handleSearch() {
  dataEditStore.fetchRawData(filters);
}

// 页面加载时自动执行一次查询
onMounted(() => {
  // 确保省份数据已加载
  statsStore.fetchAllStats();
  handleSearch();
});

// --- 表单与弹窗逻辑 ---
const isFormVisible = ref(false);
const isEditing = ref(false);
const defaultFormData = { year: 2020, province: '', city: '', county: '', yield: 0 };
const formData = reactive<RawData>({ ...defaultFormData });

// 打开表单（传入 null 则为新增，传入数据则为编辑）
function openForm(item: RawData | null) {
  if (item) {
    isEditing.value = true;
    Object.assign(formData, item); // 将选中行数据填充到表单
  } else {
    isEditing.value = false;
    Object.assign(formData, defaultFormData); // 重置为默认空表单
  }
  isFormVisible.value = true;
}

function closeForm() {
  isFormVisible.value = false;
}

// 提交表单（新增或更新）
async function submitForm() {
  const success = await dataEditStore.handleUpsert({ ...formData });
  if (success) {
    closeForm();
    handleSearch(); // 成功后刷新表格数据
  }
}

// --- 删除逻辑 ---
async function confirmDelete(item: RawData) {
  if (confirm(`确定要删除 ${item.year} 年 ${item.province} 的这条数据吗？`)) {
    const success = await dataEditStore.handleDelete({
      year: item.year,
      province: item.province,
      city: item.city,
      county: item.county
    });
    if (success) {
      handleSearch(); // 成功后刷新表格数据
    }
  }
}

// --- 导航 ---
function goBack() {
  router.push({ name: 'home' });
}
</script>

<style scoped>
.data-edit-view {
  background:  #85afd1;
  min-height: 100vh;
  padding: 24px;
  color: #e0e0e0;
}

/* 头部样式 */
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

/* 按钮通用样式 */
.action-btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #e0e0e0;
}

.action-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.back {
  background-color: #0052D9;
}

.primary {
  background-color: #a38112;
}

.success {
  background-color: #28a745;
}

.esc {
  color: black;
}

.info {
  background-color: #17a2b8;
}

.danger {
  background-color: #dc3545;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  align-items: center;
  flex-wrap: wrap;
}

.year-selector,
.province-selector {
  position: relative;
  min-width: 180px;
}

.year-selector select,
.province-selector select {
  width: 100%;
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
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23e0e0e0' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
}

.year-selector select:focus,
.province-selector select:focus {
  border-color: #0052D9;
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 82, 217, 0.2);
}

.table-container {
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.3);
  overflow: hidden;
  transition: all 0.3s ease;
}

.table-container:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  transform: translateY(-5px);
}

table {
  width: 100%;
  border-collapse: collapse;
  color: #e0e0e0;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

th {
  background-color: rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

no-data {
  text-align: center;
  padding: 20px;
  color: #aaa;
}

.actions {
  display: flex;
  gap: 8px;
}

.loading, .error {
  text-align: center;
  padding: 30px;
  font-size: 1.2em;
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.error {
  color: #ff6b6b;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: linear-gradient(135deg, #1a2a43 0%, #2f4362 100%);
  padding: 30px;
  border-radius: 16px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 24px;
  color: #e0e0e0;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #e0e0e0;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: #2f4362;
  color: #e0e0e0;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #0052D9;
  box-shadow: 0 0 0 2px rgba(0, 82, 217, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}


@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters .year-selector,
  .filters .province-selector {
    width: 100%;
  }
  
  .header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .modal-content {
    width: 90%;
    padding: 20px;
  }
}
</style>