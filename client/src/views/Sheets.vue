<template>
  <div class="sheets-container">
    <h1 class="title">Список активных листов</h1>



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
      <div v-for="item in sheets" :key="item.id" class="sheet-item border p-3 mb-3 rounded position-relative"
        :class="{ 'border-warning border-3': isUnread(item.id) }">
        <!-- Ярлык сверху -->
        <div v-if="isUnread(item.id)"
          class="position-absolute top-0 start-0 bg-warning text-dark px-3 py-1 rounded-bottom-end" style="z-index: 1;">
          <i class="bi bi-chat-left-text me-1"></i>
          Есть непрочитанные комментарии
        </div>

        <div class="row align-items-center mt-3">
          <div class="col-md-4">
            <strong>Название:</strong>
            <div class="fs-5">{{ item.name }}</div>
          </div>

          <div class="col-md-4">
            <strong>Создатель:</strong>
            <div class="fs-5">{{ usersById[item.user]?.username }}</div>
          </div>

          <div class="col-md-4">
            <strong>Статус:</strong>
            <div class="fs-5">
              <span class="badge fs-6 px-3 py-2 rounded" :class="getTotalStatusClass(item.total_status)">
                {{ item.total_status }}
              </span>
            </div>
          </div>
        </div>

        <div class="mt-3 text-end">
          <RouterLink :to="`/sheets/review/${item.id}`" class="btn btn-info">
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


const userStore = useUserStore();

const { isAuthenticated, username, role } = storeToRefs(userStore);

const sheets = ref([]);
const users = ref([]);
const sheet_unread_id = ref([]);







import TaskStatusChart from './TaskStatusChart.vue'; // импорт компонента

const analytics = ref({ total_tasks: 0, total_sheets: 0, status_counts: {} });

async function fetchAnalytics() {
  const res = await axios.get("/api/analytics/summary/");
  analytics.value = res.data;
}
const statusStats = computed(() => analytics.value.status_counts || {});
const totalTaskCount = computed(() => analytics.value.total_tasks || 0);





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
  const response = await axios.get("/api/sheets/?archived=false"); // Запрос к API
  sheets.value = response.data; // Сохраняем пользователей в переменной
}
async function fetchUnreadSheetIds() {
    const res = await axios.get("/api/comment/unread-sheets/");
    sheet_unread_id.value = res.data.sheet_ids;
  }
  function isUnread(sheetId) {
    return sheet_unread_id.value.includes(sheetId);
  }

function getTotalStatusClass(statusName) {
  switch (statusName) {
    case "Возникла проблема":
      return "bg-danger text-white"; // Красный
    case "Задерживается":
      return "bg-warning text-dark"; // Желтый
    case "Ожидание подтверждения":
      return "bg-info text-white"; // Голубой
    case "На выполнении":
      return "bg-primary text-white"; // Синий
    case "Запланировано":
      return "bg-secondary text-white"; // Серый
    case "Не актуально":
      return "bg-light text-muted"; // Светло-серый
    case "Выполнено":
      return "bg-success text-white"; // Зеленый
    default:
      return "bg-white text-muted"; // Белый для неизвестного
  }
}


onBeforeMount((async) => {
  fetchUsers();
  fetchSheets();
  fetchUnreadSheetIds();
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