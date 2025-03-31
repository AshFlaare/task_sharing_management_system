<script setup>
import { storeToRefs } from "pinia";
import { RouterLink } from "vue-router";
import useUserStore from "@/stores/userStore";

const userStore = useUserStore();
const { isAuthenticated, username, role } = storeToRefs(userStore);
</script>

<template>
  <div class="main-container">
    <h1 class="mb-4 text-center">Добро пожаловать!</h1>
    
    <div class="role-badge mb-4">
      <span class="badge" :class="{
        'bg-danger': role === 'Manager',
        'bg-primary': role === 'Executor'
      }">
        Вы вошли как: <strong>{{ role === 'Manager' ? 'Руководитель' : 'Исполнитель' }}</strong>
      </span>
    </div>

    <!-- Блок для менеджера -->
    <div v-if="role === 'Manager'" class="manager-features"> 
      <div class="row g-3">
        <div class="col-md-6">
          <div class="card h-100 feature-card">
            <div class="card-body">
              <h5 class="card-title">
                <i class="bi bi-people-fill text-danger me-2"></i>
                Управление пользователями
              </h5>
              <p class="card-text">Создание и удаление учетных записей исполнителей и руководителей</p>
              <RouterLink to="/users" class="btn btn-outline-danger">
                Перейти <i class="bi bi-arrow-right"></i>
              </RouterLink>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card h-100 feature-card">
            <div class="card-body">
              <h5 class="card-title">
                <i class="bi bi-file-earmark-plus text-danger me-2"></i>
                Создание листов заданий
              </h5>
              <p class="card-text">Формирование новых наборов задач для исполнителей</p>
              <RouterLink to="/task-sheets/create" class="btn btn-outline-danger">
                Создать <i class="bi bi-plus-lg"></i>
              </RouterLink>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card h-100 feature-card">
            <div class="card-body">
              <h5 class="card-title">
                <i class="bi bi-list-task text-danger me-2"></i>
                Активные листы
              </h5>
              <p class="card-text">Просмотр и управление текущими заданиями</p>
              <RouterLink to="/task-sheets/active" class="btn btn-outline-danger">
                Просмотреть <i class="bi bi-eye"></i>
              </RouterLink>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card h-100 feature-card">
            <div class="card-body">
              <h5 class="card-title">
                <i class="bi bi-archive text-danger me-2"></i>
                Архив листов
              </h5>
              <p class="card-text">Просмотр завершенных заданий</p>
              <RouterLink to="/task-sheets/archive" class="btn btn-outline-danger">
                Открыть архив <i class="bi bi-box-arrow-in-right"></i>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Блок для исполнителя -->
    <div v-else-if="role === 'Executor'" class="executor-features">
      
      <div class="row">
        <div class="col-md-8 mx-auto">
          <div class="card feature-card">
            <div class="card-body text-center">
              <h5 class="card-title">
                <i class="bi bi-card-checklist text-primary me-2"></i>
                Мои листы заданий
              </h5>
              <p class="card-text">Просмотр листов задач</p>
              <RouterLink to="/my-tasks" class="btn btn-primary px-4">
                <i class="bi bi-list-check me-2"></i>Перейти к листам
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.role-badge {
  text-align: center;
}

.role-badge .badge {
  font-size: 1.1rem;
  padding: 0.5rem 1rem;
}

.feature-title {
  color: var(--bs-gray-800);
  border-bottom: 2px solid var(--bs-gray-200);
  padding-bottom: 0.5rem;
}

.feature-card {
  border-radius: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.card-title i {
  font-size: 1.2em;
}

.btn-outline-danger {
  --bs-btn-hover-bg: var(--bs-danger);
}

/* Адаптивность */
@media (max-width: 768px) {
  .main-container {
    padding: 1rem;
  }
}
</style>
