<template>
    <div class="access-container">
      <div v-if="role === 'Manager'" class="manager-access">
        <h1 class="title">Список пользователей</h1>
        <div class="content">
          <!-- Здесь будет контент для менеджера -->
        </div>
      </div>
  
      <div v-else class="no-access">
        <div class="no-access-card">
          <LockIcon class="icon" />
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

  
  const userStore = useUserStore();
  const { isAuthenticated, username, role } = storeToRefs(userStore);
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
  </style>