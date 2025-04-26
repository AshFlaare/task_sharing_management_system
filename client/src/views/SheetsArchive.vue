<template>
    <div class="sheets-container">
      <h1 class="title">Список неактивных листов</h1>
      

      <!-- Только для менеджеров -->
    <div v-if="role === 'Manager'" class="mb-4">
      <h2 class="mb-3">Аналитика по задачам</h2>

      <div class="row mb-3">
        <div class="col-md-6">
          <div class="p-3 border rounded bg-light">
            <strong>Всего листов:</strong> {{ sheets.length }}<br />
            <strong>Всего задач:</strong> {{ totalTaskCount }}
          </div>
        </div>
        <div class="col-md-6">
          <TaskStatusChart :statusCounts="statusStats" />
        </div>
      </div>
    </div>


      <div class="sheets-list">
        <div v-for="item in sheets" class="sheet-item border p-3 mb-3 rounded">
          <div class="row align-items-center">
            <div class="col-md-6">
              <strong>Название:</strong>
              <div class="fs-5">{{ item.name }}</div>
            </div>
  
            <div class="col-md-6">
              <strong>Создатель:</strong>
              <div class="fs-5">{{ usersById[item.user]?.username }}</div>
            </div>
  
            
          </div>
  
          <div class="mt-3 text-end">
            <RouterLink 
              :to="`/sheets/review/${item.id}`" 
              class="btn btn-info"
            >
              <i class="bi bi-eye"></i> Просмотреть
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { storeToRefs } from "pinia";
  import { RouterLink } from "vue-router";
  import useUserStore from "@/stores/userStore";
  
  import { computed, ref, onBeforeMount, watch } from 'vue';
  import axios from "axios"
  
  import _ from 'lodash';
  import { debounce } from 'lodash';
  
  import TaskStatusChart from './TaskStatusChart.vue'; // импорт компонента

  const analytics = ref({ total_tasks: 0, total_sheets: 0, status_counts: {} });

async function fetchAnalytics() {
  const res = await axios.get("/api/analytics/summary/?archived=true");
  analytics.value = res.data;
}
const statusStats = computed(() => analytics.value.status_counts || {});
const totalTaskCount = computed(() => analytics.value.total_tasks || 0);

  
  const userStore = useUserStore();
  
  const { isAuthenticated, username, role } = storeToRefs(userStore);
  
  const sheets = ref([]);
  const users = ref([]);
  
  const usersById = computed(() => {
    return _.keyBy(users.value, x => x.id)
  })
  
  async function fetchUsers() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/users/"); // Запрос к API
    users.value = response.data; // Сохраняем пользователей в переменной
  }
  async function fetchSheets() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/sheets/?archived=true"); // Запрос к API
    sheets.value = response.data; // Сохраняем пользователей в переменной
  }
  

  
  onBeforeMount((async) => {
    fetchUsers();
    fetchSheets();
    fetchAnalytics();
  })
  </script>
  
  <style scoped>
  .sheets-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .title {
    color: #2c3e50;
    margin-bottom: 2rem;
    text-align: center;
    font-size: 2rem;
  }
  
  .sheets-list {
    width: 100%;
  }
  
  .sheet-item {
    background: white;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .sheet-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .btn-info {
    min-width: 120px;
  }
  
  .no-access .title {
    color: #e74c3c;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }
  
  .message {
    color: #7f8c8d;
    margin-bottom: 2rem;
    line-height: 1.6;
  }
  
  .home-button {
    background: #3498db;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .home-button:hover {
    background: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .sheet-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    gap: 16px;
    align-items: center;
    align-content: center;
  }
  </style>