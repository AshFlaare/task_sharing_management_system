<script setup>
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import useUserStore from "@/stores/userStore";
import { useRoute } from "vue-router";

const userStore = useUserStore();
const { isAuthenticated, username, is2Authenticated, role } = storeToRefs(userStore);
const route = useRoute();

const logout = async () => {
  userStore.logout();
};

onMounted(() => {
  userStore.checkAuthentication();
});

</script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <!-- Навигационная панель -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light px-0 shadow-sm">
      <div class="container-fluid"> <!-- Изменили на container-fluid -->
        <div class="d-flex align-items-center"> <!-- Добавили flex-контейнер -->
          <h1 class="m-0 me-3"> <!-- Добавили отступ справа -->
            <a class="navbar-brand text-dark fw-bold"><router-link to="/" class="text-dark text-decoration-none hover-primary">Система управления совместным выполнением задач</router-link></a>
          </h1>
          
          
        </div>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" 
                aria-expanded="false" 
                aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav ms-auto align-items-center">
            <li v-if="isAuthenticated" class="nav-item dropdown">
              <a class="nav-link dropdown-toggle d-flex align-items-center" 
                 href="#" role="button" data-bs-toggle="dropdown"
                 aria-expanded="false">
                <span class="me-2 fw-bold text-danger">{{ username }}</span> <!-- Жирный текст -->
                <i class="bi bi-person-circle"></i>
              </a>
              <ul class="dropdown-menu dropdown-menu-end text-center">
                <li>
                  <button class="dropdown-item d-flex justify-content-center align-items-center" @click="logout">
                    <i class="bi bi-box-arrow-right me-2"></i>
                    <span>Выход из аккаунта</span>
                  </button>
                </li>
              </ul>
            </li>
            <li v-else class="nav-item">
              <router-link class="nav-link btn btn-outline-primary" to="/login">
                Вход
              </router-link>
            </li>
          </div>
        </div>
      </div>
    </nav>

    <!-- Основной контент -->
    <main class="flex-grow-1">
      <div class="container py-4">
        <div v-if="!isAuthenticated && route.path !== '/login'" 
             class="alert alert-warning mt-3" role="alert">
          Вы не авторизованы. Пожалуйста, 
          <router-link to="/login" class="alert-link">войдите</router-link>, чтобы
          получить доступ.
        </div>
        <div v-else>
          <router-view />
        </div>
      </div>
    </main>


<!-- Подвал -->
<footer class="bg-light text-dark py-4 mt-auto border-top shadow-sm">
  <div class="container">
    <div class="row">
      <!-- Блок "О проекте" -->
      <div class="col-md-4 mb-4 mb-md-0">
        <h5 class="fw-bold mb-3">О проекте</h5>
        <p class="mb-0">Система управления совместным выполнением задач для эффективной организации работы</p>
      </div>
      
      <!-- Блок "Полезные ссылки" -->
      <div class="col-md-4 mb-4 mb-md-0">
        <h5 class="fw-bold mb-3">Полезные ссылки</h5>
        <ul class="list-unstyled">
          <li class="mb-2"><router-link to="/" class="text-dark text-decoration-none hover-primary">Главная</router-link></li>
        </ul>
      </div>
      
      <!-- Блок "Отладка" -->
      <div class="col-md-4">
        <h5 class="fw-bold mb-3">Системная информация</h5>
        <ul class="list-unstyled small">
          <li class="mb-2"><span class="text-muted">Статус: </span> 
            <span :class="{'text-success': isAuthenticated, 'text-danger': !isAuthenticated}">
              {{ isAuthenticated ? 'Авторизован' : 'Не авторизован' }}
            </span>
          </li>
          <li class="mb-2"><span class="text-muted">Пользователь:</span> {{ username || 'Гость' }}</li>
          <li class="mb-2"><span class="text-muted">Роль:</span> {{ role || 'Не определена' }}</li>
          <li class="mb-2"><span class="text-muted">Текущая страница:</span> {{ route.path }}</li>
          <li v-if="isAuthenticated">
            <button @click="logout" class="btn btn-sm btn-outline-danger p-0 border-0 text-start">
              <i class="bi bi-box-arrow-right me-1"></i>Выход из аккаунта
            </button>
          </li>
        </ul>
      </div>
    </div>
    
    
  </div>
</footer>

  </div>
</template>

<style scoped>
.navbar {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.navbar-brand {
  font-size: 1.5rem;
  transition: color 0.2s;
}

.navbar-brand:hover {
  color: #290914 !important;
}

.dropdown-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-link {
  padding: 0.5rem 1rem;
}

/* Адаптивные отступы */
@media (max-width: 992px) {
  .container-fluid {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
