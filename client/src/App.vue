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
    <!-- Навигационная панель без боковых отступов -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light px-0 shadow-sm">
      <div class="container"> <!-- Убрали горизонтальные отступы -->
        <h1 class="m-0">
          <a class="navbar-brand text-dark fw-bold" href="/">Система управления совместным выполнением задач</a>
        </h1>
        
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
                <span class="me-2">{{ username }}</span>
                <i class="bi bi-person-circle"></i>
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><button class="dropdown-item" @click="logout">
                  <i class="bi bi-box-arrow-right me-2"></i>Выход
                </button></li>
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
<footer class="bg-light text-dark py-4 mt-auto">
  <div class="container">
    <div class="row">
      <div class="col-md-4 mb-4">
        <h5>О проекте</h5>
        <p>Это система управления совместным выполнением задач</p>
      </div>
      <div class="col-md-4 mb-4">
        <h5>Полезные ссылки</h5>
        <ul class="list-unstyled">
          <li><router-link to="/" class="text-dark">Главная</router-link></li>
        </ul>
      </div>
      <div class="col-md-4">
        <h5>Отладка</h5>
        <ul class="list-unstyled ">
          <li><strong>Authenticated:</strong> {{ isAuthenticated }}</li>
          <li><strong>User:</strong> {{ username }}</li>
          <li><strong>Role:</strong> {{ role }}</li>
          <li><strong>Route:</strong> {{ route.path }}</li>
          <li><strong @click="logout" style="color: red">Выход из аккаунта</strong></li>
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
