<template>
  <div class="container py-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <div v-else-if="sheet" class="sheet-container">
      <!-- Шапка листа -->
      <div class="sheet-header bg-light p-4 rounded-top">
        <div class="d-flex justify-content-between align-items-center">
          <h1 class="mb-0">{{ sheet.name }}</h1>
          <div>
            <span class="badge bg-secondary me-2">
              Создатель: {{ usersById[sheet.user]?.username }}
            </span>
            <span class="badge bg-info me-2">
              {{ sheet.confirmed ? 'Выполнен' : 'Не выполнен' }}
            </span>
            <span class="badge bg-info me-2">
              {{ sheet.total_status }}
            </span>
          </div>
        </div>
        <div class="mt-3">
          <small class="text-muted">
            {{ console.log('creation_date:', sheet.creation_date) }}
            Создан: {{ format(new Date(sheet.creation_date), 'dd.MM.yyyy HH:mm', { locale: ru }) }}
          </small>
        </div>
      </div>

      <!-- Список задач -->
      <div class="tasks-list mt-4">
        <div v-for="(task, index) in sheet.tasks" :key="task.id" class="task-item card mb-3">
          <div class="card-header d-flex justify-content-between align-items-center"
            :class="getStatusClass(statusesById[task.status]?.name)">
            <h5 class="mb-0">Задача #{{ index + 1 }}: {{ task.name }}</h5>
            <span class="badge">
              {{ statusesById[task.status]?.name }}
            </span>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4">
                <p class="card-text">{{ task.description }}</p>
                <div class="task-meta">
                  <small class="text-muted">
                    <i class="bi bi-calendar"></i>
                    {{ format(new Date(task.date_start), 'dd.MM.yyyy HH:mm', { locale: ru }) }} -
                    {{ format(new Date(task.date_end), 'dd.MM.yyyy HH:mm', { locale: ru }) }}
                  </small>
                </div>
              </div>
              <div class="col-md-4">
                <div class="executor-info">
                  <h6>Текущий статус:</h6>
                  <div v-if="task.status" class="d-flex align-items-center mt-2">
                    <div>
                      <strong>{{ statusesById[task.status]?.name }}</strong>
                    </div>
                  </div>
                  <div v-else class="text-muted">Нет статуса</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="executor-info">
                  <h6>Исполнитель:</h6>
                  <div v-if="task.user" class="d-flex align-items-center mt-2">
                    <div>
                      <strong>{{ usersById[task.user]?.username }}</strong>
                      <div class="text-muted small">{{ usersById[task.user]?.email }}</div>
                    </div>
                  </div>
                  <div v-else class="text-muted">Не назначен</div>
                </div>
              </div>
            </div>

            <!-- Блок комментариев -->
            <div class="comments-section mt-4">
              <h6 class="border-bottom pb-2">Комментарии:</h6>


              <div v-if="task.comments && task.comments.length > 0" class="comments-list">
                <div v-for="comment in task.comments" :key="comment.id" :class="['comment-item mb-3 ps-3 border-start', {
                  'bg-warning-subtle border-warning': isUnread(comment, task)
                }]">
                  <div class="d-flex justify-content-between">
                    <strong>{{ usersById[comment.user]?.username }}</strong>
                    <small class="text-muted">
                      {{ format(new Date(comment.date), 'dd.MM.yyyy HH:mm', { locale: ru }) }}
                    </small>
                  </div>
                  <p class="mb-0 mt-1">{{ comment.text }}</p>
                </div>
              </div>
              <div v-else class="text-muted small">
                Нет комментариев
              </div>

              <!-- Форма добавления комментария -->
              <div v-if="!sheet.confirmed" class="add-comment mt-3">
                <div
                  v-if="(task.user == userId || isManager) && statusesById[task.status]?.name !== 'Выполнено' && statusesById[task.status]?.name !== 'Не актуально'">
                  <textarea v-model="newComments[task.id]" class="form-control mb-2"
                    placeholder="Введите комментарий..." rows="2"></textarea>
                  <button class="btn btn-sm btn-primary me-2" @click="addComment(task.id)">
                    <i class="bi bi-send"></i> Добавить комментарий
                  </button>
                  <button v-if="!isManager && task.user === userId" class="btn btn-sm btn-outline-success me-2"
                    @click="onStatusEditClick(task)" data-bs-toggle="modal" data-bs-target="#editStatusModal">
                    <i class="bi bi-arrow-repeat"></i> Изменить статус задачи
                  </button>
                  <button class="btn btn-sm btn-outline-secondary me-2" v-if="hasUnreadComments(task.comments, task)"
                    @click="markCommentsAsRead(task.id)">
                    <i class="bi bi-eye"></i> Прочитать все
                  </button>
                </div>

              </div>
              <!-- Если лист архивный, то скрыть добавление комментария -->
              <div v-else class="text-muted small">
                Новые комментарии запрещены для архивного листа.
              </div>
            </div>
          </div>
          <div v-if="isManager && !sheet.confirmed" class=" card-footer text-end">
            <button class="btn btn-sm btn-outline-primary me-2" @click="onTaskEditClick(task)" data-bs-toggle="modal"
              data-bs-target="#editTaskModal">
              <i class="bi bi-pencil"></i> Изменить
            </button>

          </div>

        </div>
      </div>







      <div class="modal fade" id="editTaskModal" tabindex="-1" aria-labelledby="editTaskModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header bg-light">
              <h5 class="modal-title fw-bold" id="editTaskModalLabel">Редактирование задачи</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="onUpdateTask">
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <div class="form-floating mb-3">
                      <input type="text" class="form-control" id="editTaskName" v-model="taskToEdit.name" required>
                      <label for="editTaskName">Название задачи</label>
                    </div>

                    <div class="form-floating mb-3">
                      <textarea class="form-control" id="editTaskDescription" v-model="taskToEdit.description"
                        style="height: 100px;"></textarea>
                      <label for="editTaskDescription">Описание</label>
                    </div>

                    <div class="form-floating mb-3">
                      <input type="datetime-local" class="form-control" id="editDateStart"
                        v-model="taskToEdit.date_start">
                      <label for="editDateStart">Дата начала</label>
                    </div>

                    <div class="form-floating mb-3">
                      <input type="datetime-local" class="form-control" id="editDateEnd" v-model="taskToEdit.date_end">
                      <label for="editDateEnd">Дата окончания</label>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-floating mb-3">
                      <select class="form-select" id="editTaskUser" v-model="taskToEdit.user">
                        <option :value="null">Не назначен</option>
                        <option v-for="user in executors" :key="user.id" :value="user.id">
                          {{ user.username }} ({{ user.email }}) - {{ user.position }} - {{ user.active_tasks_count }}
                          активных / {{ user.all_tasks_count }} всего
                        </option>
                      </select>
                      <label for="editTaskUser">Исполнитель</label>
                    </div>

                    <div class="form-floating mb-3">
                      <select class="form-select" id="editTaskStatus" v-model="taskToEdit.status">
                        <option v-for="status in aviable_statuses" :key="status.id" :value="status.id">
                          {{ status.name }}
                        </option>
                      </select>
                      <label for="editTaskStatus">Статус</label>
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                @click="onUpdateTask">Сохранить</button>
            </div>
          </div>
        </div>
      </div>










      <div class="modal fade" id="editStatusModal" tabindex="-1" aria-labelledby="editStatusModalLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header bg-light">
              <h5 class="modal-title fw-bold" id="editStatusModalLabel">Изменить статус</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="onUpdateTask">
                <div class="row g-3 mb-4">
                  <div class="col-md-12">
                    <div class="form-floating mb-3">
                      <select class="form-select" id="editTaskStatus" v-model="taskToEdit.status">
                        <option v-for="status in aviable_statuses" :key="status.id" :value="status.id">
                          {{ status.name }}
                        </option>
                      </select>
                      <label for="editTaskStatus">Статус</label>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                @click="onUpdateTask">Сохранить</button>
            </div>
          </div>
        </div>
      </div>








      <div class="modal fade" id="taskCreateModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <form @submit.prevent="onCreateTask">
            <div class="modal-content p-3">
              <h5>Новая задача</h5>

              <div class="form-floating mb-2">
                <input type="text" class="form-control" v-model="newTask.name" required />
                <label>Название задачи</label>
              </div>

              <div class="form-floating mb-2">
                <input type="text" class="form-control" v-model="newTask.description" required />
                <label>Описание</label>
              </div>

              <div class="form-floating mb-2">
                <input type="datetime-local" class="form-control" v-model="newTask.date_start" required />
                <label>Начало</label>
              </div>

              <div class="form-floating mb-2">
                <input type="datetime-local" class="form-control" v-model="newTask.date_end" required />
                <label>Окончание</label>
              </div>

              <div class="form-floating mb-3">
                <select class="form-select" v-model="newTask.user" required>
                  <option :value="null">Не назначено</option>
                  <option v-for="executor in executors" :key="executor.id" :value="executor.id">
                    {{ executor.username }} ({{ executor.email }}) - {{ executor.position }} - {{
                    executor.active_tasks_count }} активных / {{ executor.all_tasks_count }} всего
                  </option>
                </select>
                <label>Исполнитель</label>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                <button type="submit" class="btn btn-primary" data-bs-dismiss="modal" @click="onTaskAddClick()">Создать</button>
              </div>


            </div>
          </form>
        </div>
      </div>










      <!-- Кнопки действий -->
      <div class="actions mt-4">
        <router-link :to="sheet.confirmed ? '/sheets-archive/review' : '/sheets/review'" class="btn btn-secondary me-2">
          <i class="bi bi-arrow-left"></i> Назад к списку
        </router-link>
        <button v-if="isManager && !sheet.confirmed" class="btn btn-info me-2" data-bs-toggle="modal"
          data-bs-target="#taskCreateModal">
          <i class="bi bi-arrow-90deg-up"></i> Добавить задачу в лист
        </button>
        <button v-if="isManager && !sheet.confirmed" class="btn btn-success me-2" @click="confirmSheet">
          <i class="bi bi-check-circle"></i> Подтвердить лист
        </button>

      </div>
    </div>

    <div v-else class="alert alert-danger">
      Лист задач не найден
    </div>
  </div>
</template>

<script setup>

import { storeToRefs } from "pinia";
import { RouterLink, useRoute } from "vue-router"; // Добавлен useRoute
import useUserStore from "@/stores/userStore";

import { computed, ref, onBeforeMount, watch } from 'vue';
import axios from "axios";


import _ from 'lodash';
import { debounce } from 'lodash';


import { format } from 'date-fns'
import { ru } from 'date-fns/locale'


const userStore = useUserStore();
const route = useRoute(); // Получаем текущий маршрут
const users = ref([])
const statuses = ref([])
var aviable_statuses = ref([])
const executors = ref([])
const { userId, isAuthenticated, username, role } = storeToRefs(userStore);

const taskToEdit = ref([]);

const newTask = ref({})

const sheet = ref(null)
const loading = ref(true)

const isManager = computed(() => role.value === 'Manager')
async function fetchUsers() {
  // Выполняем запрос для получения всех пользователей
  const response = await axios.get("/api/userssafe/"); // Запрос к API
  users.value = response.data; // Сохраняем пользователей в переменной
}
const usersById = computed(() => {
  return _.keyBy(users.value, x => x.id)
})
async function fetchStatuses() {
  const response = await axios.get("/api/status/");
  statuses.value = response.data;
}
const statusesById = computed(() => {
  return _.keyBy(statuses.value, x => x.id)
})

const newComments = ref({})
async function onTaskAddClick() {
  try {
    // Сначала создаём задачу
    const response = await axios.post(`/api/sheets/${sheet.value.id}/tasks/`, {
      ...newTask.value
    });

    const createdTask = response.data; // Здесь содержится ID новой задачи

    // Затем создаём комментарий
    await axios.post('/api/comment/write/', {
      text: 'Задача создана',
      task: createdTask.id
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    alert('Задача добавлена!');
    await fetchSheet(); // или fetchTasks()

  } catch (err) {
    console.error(err);
    alert('Ошибка при создании задачи');
  }
}
async function addComment(taskId) {
  try {
    const commentText = newComments.value[taskId]?.trim();

    if (!commentText) {
      alert('Введите текст комментария');
      return;
    }

    const payload = {
      text: commentText,
      task: taskId
    };

    // Отправляем комментарий на сервер
    const response = await axios.post('/api/comment/write/', payload, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    // Находим задачу в текущем состоянии
    const taskToUpdate = sheet.value.tasks.find(t => t.id === taskId);

    if (taskToUpdate) {
      // Создаем новый массив комментариев с добавленным комментарием
      const updatedComments = [
        ...(taskToUpdate.comments || []),
        {
          ...response.data,
          user: userId,
          date: new Date().toISOString()
        }
      ];

      // Обновляем локальное состояние
      taskToUpdate.comments = updatedComments;
    }

    // Очищаем поле ввода
    newComments.value[taskId] = '';

    console.log('Комментарий добавлен:', response.data);

  } catch (error) {
    console.error('Ошибка:', error);

    if (error.response?.status === 401) {
      alert('Необходимо авторизоваться для добавления комментариев');
    } else {
      alert('Ошибка: ' + (error.response?.data?.detail || error.message));
    }
  }
}

const fetchSheet = async () => {
  loading.value = true;
  try {
    // Делаем запросы параллельно для ускорения загрузки
    const [tasksResponse, sheetResponse] = await Promise.all([
      axios.get(`/api/sheets/${route.params.id}/tasks`),
      axios.get(`/api/sheets/${route.params.id}`)
    ]);

    // Объединяем данные
    sheet.value = {
      ...sheetResponse.data, // Основная информация о листе
      tasks: tasksResponse.data // Массив задач
    };

    console.log('Загруженные данные:', sheet.value);
  } catch (error) {
    console.error('Ошибка загрузки:', error);
    // Можно добавить обработку ошибки в UI
    sheet.value = null;
  } finally {
    loading.value = false;
  }
};



function isUnread(comment, task) {

  
  if (role.value == 'Manager') {
    return (
      (!comment.read && (comment.user != userId.value))
    );
  }
  else {
    return (
      !comment.read && (comment.user != userId.value) && task.user == userId.value
    );
  }
}
function hasUnreadComments(comments, task) {
  if (role.value == 'Manager') {
    return (
      comments.some(c => !c.read && c.user !== userId.value)
    );
  }
  else {
    return (
      comments.some(c => !c.read && c.user !== userId.value) && task.user == userId.value
    );
  }

  
}

async function markCommentsAsRead(taskId) {
  try {
    const response = await axios.post('/api/comment/mark-read/', { task_id: taskId });
    await fetchSheet();
    console.log(response.data); // { status: "Comments marked as read" }
  } catch (err) {
    console.error('Ошибка при пометке комментариев как прочитанных:', err);
  }
}



function getAvailableStatuses(currentStatus) {
  if (role.value === 'Manager') {
    // Логика для менеджера
    if (currentStatus === 'Выполнено') {
      return statuses.value.filter(status => status.name === 'Ожидание подтверждения' || status.name === 'Не актуально');
    } else if (currentStatus === 'Возникла проблема') {
      return statuses.value.filter(status => status.name === 'Не актуально' || status.name === 'Ожидание подтверждения');
    } else if (currentStatus === 'На выполнении') {
      return statuses.value.filter(status => status.name === 'Не актуально');
    }
  } else if (role.value === 'Executor') {
    // Логика для исполнителя
    if (currentStatus === 'Ожидание подтверждения') {
      return statuses.value.filter(status => status.name === 'Возникла проблема' || status.name === 'На выполнении');
    } else if (currentStatus === 'На выполнении') {
      return statuses.value.filter(status => status.name === 'Выполнено' || status.name === 'Возникла проблема');
    } else if (currentStatus === 'Возникла проблема') {
      return statuses.value.filter(status => status.name === 'На выполнении');
    }
  }
  return statuses.value; // Если нет ограничения, показываем все статусы
}



const confirmSheet = async () => {
  try {
    // Используем PATCH для изменения состояния листа
    await axios.patch(`/api/task-sheets/${route.params.id}/confirm/`, {
      confirmed: true
    })
    sheet.value.confirmed = true
  } catch (error) {
    console.error('Ошибка подтверждения:', error)
  }
}



function toDateTimeLocalString(date) {
  if (!date) return '';
  const d = new Date(date);
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); // сдвигаем по UTC
  return d.toISOString().slice(0, 16); // YYYY-MM-DDTHH:MM
}
async function onTaskEditClick(task) {
  taskToEdit.value = { ...task };
  taskToEdit.value.date_start = toDateTimeLocalString(task.date_start);
  taskToEdit.value.date_end = toDateTimeLocalString(task.date_end);
  aviable_statuses = getAvailableStatuses(statusesById.value[task.status]?.name);
}

async function onStatusEditClick(task) {
  taskToEdit.value = { ...task }; // Копируем task в taskToEdit
  aviable_statuses = getAvailableStatuses(statusesById.value[task.status]?.name);
}



async function onUpdateTask() {
  const sheetId = taskToEdit.value.sheet;
  const taskId = taskToEdit.value.id;

  try {
    // Обновляем задачу
    await axios.put(`/api/sheets/${sheetId}/tasks/${taskId}/`, {
      ...taskToEdit.value
    });

    var systemComment;
    // Добавляем системный комментарий
    if (role.value == 'Manager') {
      systemComment = {
      text: '<Данные задачи были изменены руководителем>',
      task: taskId
    };}
    else {
      systemComment = {
      text: '<Статус задачи был изменен исполнителем>',
      task: taskId
    }
  }

    await axios.post('/api/comment/write/', systemComment, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    await fetchSheet(); // Перезагрузка данных

  } catch (error) {
    console.error('Ошибка при обновлении задачи:', error);
    alert('Не удалось обновить задачу');
  }
}
async function fetchExecutors() {
  // Выполняем запрос для получения всех пользователей
  const response = await axios.get("/api/executors/"); // Запрос к API
  executors.value = response.data; // Сохраняем пользователей в переменной
}
function getStatusClass(statusName) {

  console.log(statusName)
  switch (statusName) {
    case "Возникла проблема":
      return "bg-danger text-white";
    case "Задерживается":
      return "bg-warning text-dark";
    case "Ожидание подтверждения":
      return "bg-info text-white";
    case "На выполнении":
      return "bg-primary text-white";
    case "Запланировано":
      return "bg-secondary text-white";
    case "Не актуально":
      return "bg-light text-muted";
    case "Выполнено":
      return "bg-success text-white";
    default:
      return "bg-white";
  }
}

onBeforeMount((async) => {
  fetchSheet();
  fetchUsers();
  fetchStatuses();
  fetchExecutors();

})



</script>

<style scoped>
.sheet-container {
  max-width: 1200px;
  margin: 0 auto;
}

.sheet-header {
  border: 1px solid #dee2e6;
  border-bottom: none;
}

.task-item {
  border-radius: 0.25rem;
}

.task-item .card-header {
  background-color: #f8f9fa;
}

.actions {
  padding: 1rem;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
}
</style>