<template>
  <div class="access-container">
    <div v-if="role === 'Manager'" class="manager-access">
      <h1 class="title">Список пользователей</h1>
      <div class="content">
        <!-- Здесь будет контент для менеджера -->


        <div class="container-fluid">
          <div class="p-2">
            <form @submit.prevent.stop="onUserAdd" class="p-4 shadow-sm rounded bg-light">
              <div class="row g-3">

                <div class="col-md-2">
                  <div class="form-floating">
                    <input type="text" id="user_name" class="form-control" v-model="userToAdd.username" required>
                    <label for="user_name">ФИО</label>
                  </div>
                </div>


                <div class="col-md-2">
                  <div class="form-floating">
                    <input type="text" id="user_position" class="form-control" v-model="userToAdd.position" required>
                    <label for="position">Должность</label>
                  </div>
                </div>

                <div class="col-md-2">
                  <div class="form-floating">
                    <input type="email" id="user_email" class="form-control" :class="{'is-invalid': emailError}"
                      v-model="userToAdd.email" required @input="emailError = ''">
                    <label for="user_email">Почта</label>
                    <div v-if="emailError" class="invalid-feedback">
                      {{ emailError }}
                    </div>
                  </div>
                </div>

                <div class="col-md-2">
                  <div class="form-floating">
                    <input type="text" id="user_phone" class="form-control" v-model="userToAdd.phone" required>
                    <label for="user_phone">Телефон</label>
                  </div>
                </div>

                <div class="col-md-2">
                  <div class="form-floating">
                    <input type="text" id="user_password" class="form-control" v-model="userToAdd.password" required>
                    <label for="user_password">Пароль</label>
                  </div>
                </div>

                <div class="col-md-2">
                  <div class="form-floating">
                    <select id="user_role" class="form-select" v-model="userToAdd.role" required>
                      <option :value="r.id" v-for="r in roles" :key="r.id">{{ r.name }}</option>
                    </select>
                    <label for="user_role">Роль</label>
                  </div>
                </div>




                <!-- Кнопка -->
                <div class="col-12 text-end">
                  <button class="btn btn-primary">
                    <i class="bi bi-plus-circle"></i> Добавить пользователя
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>








        <div>
          <div v-for="item in users" class="user-item border p-3 mb-3">
            <div class="row">

              <div class="col-3">
                <strong>ФИО:</strong>
                <div>{{ item.username }}</div>
              </div>
            

            <div class="col-3">
              <strong>Должность:</strong>
              <div>{{ item.position }}</div>
          </div>

          <div class="col-2">
            <strong>Почта:</strong>
            <div>{{ item.email }}</div>
          </div>

          <div class="col-2">
            <strong>Телефон:</strong>
            <div>{{ item.phone }}</div>
          </div>

          <div class="col-2">
            <strong>Роль:</strong>
            <div>{{ rolesById[item.role]?.name }}</div>
          </div>



          <!-- Кнопки редактирования и удаления -->
          <div class="col-12 mt-2 d-flex justify-content-end gap-2">
            <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editUserModal"
                @click="onUserEditClick(item)">
                <i class="bi bi-pencil"></i> Редактировать
            </button>
            <button class="btn btn-danger" data-bs-toggle="modal"
                data-bs-target="#deleteConfirmationModalRef" @click="onUserDeleteClick(item)">
                <i class="bi bi-file-earmark-minus"></i> Удалить
            </button>
        </div>



        </div>



          </div>
        </div>





<!-- Modal for User Editing -->
<div class="modal fade" id="editUserModal" tabindex="-1" aria-labelledby="editUserModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
      <div class="modal-content">
          <div class="modal-header bg-light">
              <h5 class="modal-title fw-bold" id="editUserModalLabel">Редактирование пользователя</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
              <form @submit.prevent="onUpdateUser">
                  <div class="row g-3 mb-4">
                      <!-- Основная информация -->
                      <div class="col-md-6">
                          <div class="form-floating mb-3">
                              <input type="text" class="form-control" id="editUsername" 
                                     v-model="userToEdit.username" required>
                              <label for="editUsername">ФИО</label>
                          </div>
                          
                          <div class="form-floating mb-3">
                              <input type="text" class="form-control" id="editPosition" 
                                     v-model="userToEdit.position" required>
                              <label for="editPosition">Должность</label>
                          </div>
                          
                          <div class="form-floating mb-3">
                              <input type="email" class="form-control" id="editEmail" 
                                     v-model="userToEdit.email" required>
                              <label for="editEmail">Email</label>
                          </div>
                      </div>
                      
                      <div class="col-md-6">
                          <div class="form-floating mb-3">
                              <input type="tel" class="form-control" id="editPhone" 
                                     v-model="userToEdit.phone" required>
                              <label for="editPhone">Телефон</label>
                          </div>
                          
                          <div class="form-floating mb-3">
                              <select class="form-select" id="editRole" v-model="userToEdit.role" required>
                                  <option v-for="role in roles" :value="role.id" :key="role.id">
                                      {{ role.name }}
                                  </option>
                              </select>
                              <label for="editRole">Роль</label>
                          </div>
                      </div>
                  </div>
                  
                  <!-- Смена пароля -->
                  <div class="card mb-4">
                      <div class="card-header bg-light fw-bold">Смена пароля</div>
                      <div class="card-body">
                          <div class="form-floating mb-3">
                              <input type="password" class="form-control" id="password" 
                                     v-model="userToEdit.password" placeholder="Оставьте пустым, если не нужно менять">
                              <label for="password">Новый пароль</label>
                          </div>
                      
                          <small class="text-muted">Оставьте пустым, если не требуется смена пароля</small>
                      </div>
                  </div>
              </form>
          </div>
          <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateUser">Сохранить изменения</button>
          </div>
      </div>
  </div>
</div>



<!-- Modal для подтверждения удаления -->
<div class="modal fade" id="deleteConfirmationModalRef" tabindex="-1" role="dialog"
aria-labelledby="deleteModalLabel" aria-hidden="true">
<div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="deleteModalLabel">Подтверждение удаления</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
            Вы уверены, что хотите удалить этого пользователя?
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                @click="onRemoveClick(userToDelete)">Удалить</button>
        </div>
    </div>
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
const { isAuthenticated, username, role } = storeToRefs(userStore);

const users = ref([]);
const roles = ref([]);
const userToAdd = ref([]);
const userToEdit = ref([]);
const userToDelete = ref([]);



const emailError = ref("");
const submitError = ref("");


async function fetchUsers() {
  // Выполняем запрос для получения всех пользователей
  const response = await axios.get("/api/users/"); // Запрос к API
  users.value = response.data; // Сохраняем пользователей в переменной
}
async function fetchRoles() {
    const r = await axios.get("/api/roles/");
    roles.value = r.data;
}
const rolesById = computed(() => {
  return _.keyBy(roles.value, x => x.id)
})



async function onUserAdd() {
  // Сбрасываем ошибки
  emailError.value = "";
  submitError.value = "";
  
  try {
    console.log(userToAdd.value);
    await axios.post("/api/users/", {
      ...userToAdd.value,
    });
    
    // Сброс формы после успешного создания
    userToAdd.value = {
      username: "",
      position: "",
      email: "",
      phone: "",
      password: "",
      role: ""
    };
    
    await fetchUsers();
    
  } catch (error) {
    if (error.response) {
      // Обработка ошибки валидации email
      if (error.response.data.email) {
        emailError.value = error.response.data.email[0];
      }
      // Обработка других ошибок
      else if (error.response.data.detail) {
        submitError.value = error.response.data.detail;
      } else {
        submitError.value = "Произошла ошибка при создании пользователя";
      }
    } else {
      submitError.value = "Ошибка сети или сервера";
    }
    console.error("Ошибка при создании пользователя:", error);
  }
}
async function onUpdateUser() {
    await axios.put(`/api/users/${userToEdit.value.id}/`, {
        ...userToEdit.value
    });
    await fetchUsers();
}
async function onUserEditClick(user) {
    userToEdit.value = { ...user };
}
async function onRemoveClick(user) {
    await axios.delete(`/api/users/${user.id}/`);
    userToDelete.value = null;
    await fetchUsers();
}
async function onUserDeleteClick(user) {
    userToDelete.value = { ...user };
}


onBeforeMount((async) => {
  fetchUsers();
  fetchRoles();
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
.user-item {
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