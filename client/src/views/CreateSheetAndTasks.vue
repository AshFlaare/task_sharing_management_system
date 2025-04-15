<template>
    <div class="access-container">
        <div v-if="role === 'Manager'" class="manager-access">
            <h1 class="title">Создать лист задач</h1>
            <div class="content">
              <div class="container-fluid">
                <div class="p-2">
                  <form @submit.prevent.stop="onSheetAdd" class="p-4 shadow-sm rounded bg-light">
                    <div class="row g-3">
                      <div class="col-md-12">
                        <div class="form-floating">
                          <input type="text" id="sheet_name" class="form-control" v-model="sheetToAdd.name" required>
                          <label for="name">Название листа</label>
                        </div>
                      </div>
          
                      <!-- Задачи -->
                      <div class="col-md-12">
                        <div class="card mb-3" v-for="(task, index) in sheetToAdd.tasks" :key="index">
                          <div class="card-header d-flex justify-content-between align-items-center">
                            <span>Задача #{{ index + 1 }}</span>
                            <button type="button" class="btn btn-sm btn-danger" @click="removeTask(index)" 
                                    v-if="sheetToAdd.tasks.length > 1">
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>
                          <div class="card-body">
                            <div class="row g-3">
                              <div class="col-md-4">
                                <div class="form-floating">
                                  <input type="text" class="form-control" v-model="task.name" required>
                                  <label>Название задачи</label>
                                </div>
                              </div>
                              <div class="col-md-4">
                                <div class="form-floating">
                                  <input type="text" class="form-control" v-model="task.description" required>
                                  <label>Описание</label>
                                </div>
                              </div>
                              <div class="col-md-2">
                                <div class="form-floating">
                                  <input type="datetime-local" class="form-control" v-model="task.date_start" required>
                                  <label>Начало</label>
                                </div>
                              </div>
                              <div class="col-md-2">
                                <div class="form-floating">
                                  <input type="datetime-local" class="form-control" v-model="task.date_end" required>
                                  <label>Окончание</label>
                                </div>
                              </div>
                              <div class="col-md-12">
                                <div class="form-floating">
                                  <select class="form-select" v-model="task.executor" required>
                                    <option :value="null">Не назначено</option>
                                    <option 
                                      v-for="executor in executors" 
                                      :key="executor.id" 
                                      :value="executor.id"
                                      :title="`${executor.username} (${executor.email}) • ${executor.position} • ${executor.active_tasks_count} активных • ${executor.all_tasks_count} всего`"
                                    >
                                      {{ executor.username }} ({{ executor.email }}) - {{ executor.position }} - {{ executor.active_tasks_count }} активных / {{ executor.all_tasks_count }} всего
                                    </option>
                                  </select>
                                  <label>Исполнитель</label>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
          
                        <div class="col-12 text-end">
                        <button type="button" class="btn btn-success mt-2" @click="addTask">
                          <i class="bi bi-plus-circle"></i> Добавить задачу
                        </button>
                    </div>
                      </div>
          
                      <!-- Кнопка создания -->
                      <div class="col-12 text-end">
                        <button type="submit" class="btn btn-primary">
                          <i class="bi bi-save"></i> Создать лист
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          
    </div>

    <div v-else class="no-access">
      <div class="no-access-card">

        <h2 class="title">Доступ запрещён</h2>
        <p class="message">
          У вас недостаточно прав для просмотра этой страницы.
        </p>
        <RouterLink to="/" class="home-link">
          <button class="home-button">На главную</button>
        </RouterLink>
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

const { userId, isAuthenticated, username, role } = storeToRefs(userStore);


const sheetToAdd = ref({
  name: '',
  tasks: [{
    name: '',
    description: '',
    date_start: '',
    date_end: '',
    user: null
  }]
});

const executors = ref([]); // Заполняется из API

async function fetchExecutors() {
  // Выполняем запрос для получения всех пользователей
  const response = await axios.get("/api/executors/"); // Запрос к API
  executors.value = response.data; // Сохраняем пользователей в переменной

  // Тут еще надо получать инфу о активных и всех задачах и складывать с инфой выше
  // Или добавить в уже существующий апишник расчет количества задач
  // Но модель указана юзер, из задач надо брать даты

}

// Добавление новой задачи
// Добавление новой задачи
function addTask() {
  sheetToAdd.value.tasks.push({
    name: '',
    description: '',
    date_start: '',
    date_end: '',
    executor: null
  });
}

// Удаление задачи
function removeTask(index) {
  sheetToAdd.value.tasks.splice(index, 1);
}

// Отправка данных
async function onSheetAdd() {
  try {
    //console.log(userId.value)
    // Подготовка данных для отправки
    const payload = {
      name: sheetToAdd.value.name,
      user: userId.value, // ID текущего пользователя (руководителя)
      tasks: sheetToAdd.value.tasks.map(task => ({
        name: task.name,
        description: task.description,
        date_start: task.date_start,
        date_end: task.date_end,
        user: task.executor // ID исполнителя
      }))
    };

    console.log(payload)
    const response = await axios.post('/api/task-sheets/', payload);
    
    // Очистка формы после успешного создания
    sheetToAdd.value = {
      name: '',
      tasks: [{
        name: '',
        description: '',
        date_start: '',
        date_end: '',
        executor: null
      }]
    };
    
    alert('Лист задач успешно создан!');
    console.log('Создан лист задач:', response.data);
    
  } catch (error) {
    console.error('Ошибка:', error.response?.data || error.message);
    alert('Произошла ошибка при создании листа задач');
  }
}
onBeforeMount((async) => {
fetchExecutors();
})
</script>

<style scoped>
.access-container {
    min-height: 70vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }
  
  .manager-access {
    width: 100%;
    max-width: 1200px;
  }
  
  .title {
    color: #2c3e50;
    margin-bottom: 2rem;
    text-align: center;
  }
  
  .no-access {
    animation: fadeIn 0.5s ease-out;
  }
  
  .no-access-card {
    background: white;
    border-radius: 12px;
    padding: 2.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    text-align: center;
    max-width: 450px;
    margin: 0 auto;
  }
  
  .icon {
    width: 64px;
    height: 64px;
    margin-bottom: 1.5rem;
    color: #e74c3c;
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

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
  
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .executor-option {
    padding: 8px 12px;
    border-bottom: 1px solid #eee;
  }
  
  .executor-option small {
    opacity: 0.7;
    font-size: 0.9em;
  }
  
  .executor-option .badge {
    font-size: 0.8em;
    padding: 2px 6px;
    margin: 0 2px;
  }
</style>>
