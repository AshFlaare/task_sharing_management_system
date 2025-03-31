<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from "axios";
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import useUserStore from '@/stores/userStore';

const username = ref("");
const pass = ref("");
const errorMessage = ref("");
const userStore = useUserStore();
const { isAuthenticated } = storeToRefs(userStore);
const router = useRouter();

async function login() {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
  // if (!csrfToken) {
  //   errorMessage.value = "Ошибка: CSRF-токен отсутствует.";
  //   return;
  // }

  errorMessage.value = "";
  try {
    const response = await axios.post(
      "/api/user/login/",
      {
        username: username.value,
        password: pass.value,
        //otp_key: "TEST",

      },
      {
        headers: {
          'X-CSRFToken': csrfToken,
        },
      }
    );

    if (response.data.success) {
      await userStore.fetchUser(); // Обновляем данные о пользователе
    } else {
      errorMessage.value = response.data.error || "Неверные учетные данные.";
    }
  } catch (error) {
    console.error(error); // Для диагностики ошибок
    errorMessage.value = "Ошибка входа. Попробуйте позже.";
  }
}

onMounted(() => {
  if (isAuthenticated.value) {
    router.push("/");
  }
});


watch(isAuthenticated, (newVal) => {
  if (newVal) {
    router.push("/"); // Перенаправляем на главную страницу после изменения isAuthenticated
  }
});

onMounted(() => {
  if (isAuthenticated.value) {
    router.push("/"); // Перенаправляем, если пользователь уже аутентифицирован
  }
});
</script>


<template>
  
  <div class="login-container">
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="username" class="form-label">Электронная почта</label>
        <input
          type="text"
          id="username"
          class="form-control"
          v-model="username"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Пароль</label>
        <input
          type="password"
          id="password"
          class="form-control"
          v-model="pass"
          required
        />
      </div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <button type="submit" class="btn btn-primary">Войти</button>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin-top: 50px;
  margin: auto;
  padding: 20px;
  
  background-color: rgb(255, 255, 255)
}

.login-container h2 {
  margin-bottom: 20px;
}

.login-container .form-label {
  font-weight: bold;
}

.login-container .btn {
  width: 100%;
}
</style>
