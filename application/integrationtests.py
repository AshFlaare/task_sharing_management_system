import requests
import sys
import os

# Настройка базового URL в зависимости от окружения
if 'JENKINS_URL' in os.environ:
    # В Jenkins используем тестовый сервер
    BASE_URL = 'http://test-server:8000'
else:
    # Локально используем localhost
    BASE_URL = 'http://localhost:8000'

REGISTER_URL = f'{BASE_URL}/api/users/'
LOGIN_URL = f'{BASE_URL}/api/user/login/'
LOGOUT_URL = f'{BASE_URL}/api/user/logout/'
ROLES_URL = f'{BASE_URL}/api/roles/'
TASKSHEET_URL = f'{BASE_URL}/api/task-sheets/'
EXECUTOR_SHEETS_URL = f'{BASE_URL}/api/my-sheets/review/'

# URL для удаления (проверьте правильность endpoints!)
DELETE_USER_URL = f'{BASE_URL}/api/users/{{id}}/'
DELETE_SHEET_URL = f'{BASE_URL}/api/sheet/{{id}}/'  # Исправлено на task-sheets

# Глобальные переменные для хранения созданных тестовых данных
test_users = []
test_sheets = []

def login(username, password):
    session = requests.Session()
    res = session.post(LOGIN_URL, json={
        "username": username,
        "password": password
    })

    assert res.status_code == 200 and res.json().get("success"), "Ошибка при входе"
    return session

def logout(session):
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {
        "X-CSRFToken": csrf_token,
        "username": "",
        "password": "", 
    }
    res = session.post(LOGOUT_URL, headers=headers)
    if res.status_code != 200:
        print("Ответ при logout:")
        print(f"Статус: {res.status_code}")
        print(f"Ответ: {res.text[:500]}")
    assert res.status_code == 200, "Не удалось выйти из аккаунта"

def get_roles(session):
    res = session.get(ROLES_URL)
    assert res.status_code == 200, "Не удалось получить список ролей"
    roles = res.json()
    return {role["name"]: role["id"] for role in roles}

def register_user(session, username, email, password, position, role_id):
    headers = {
        "X-CSRFToken": session.cookies.get("csrftoken", "")
    }
    res = session.post(REGISTER_URL, json={
        "username": username,
        "email": email,
        "password": password,
        "position": position,
        "role": role_id,
        "phone": "+70000000001"
    }, headers=headers)

    if res.status_code != 201:
        print(f"Ответ сервера при попытке зарегистрировать {username}:")
        print(f"Статус: {res.status_code}")
        print(f"Ответ: {res.text}")
    assert res.status_code == 201, f"Ошибка при регистрации пользователя {username}"
    
    user_data = res.json()
    test_users.append(user_data)
    return user_data

def get_executor_sheets(session):
    res = session.get(EXECUTOR_SHEETS_URL)
    assert res.status_code == 200, "Ошибка при получении листов исполнителя"
    return res.json()

def delete_user(session, user_id):
    """Удаление пользователя по ID"""
    if user_id == 1:  # Не удаляем администратора
        print(f"Пропускаем удаление администратора (ID: {user_id})")
        return False
    
    url = DELETE_USER_URL.format(id=user_id)
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {"X-CSRFToken": csrf_token}
    
    res = session.delete(url, headers=headers)
    
    if res.status_code == 204:
        print(f"Пользователь ID {user_id} удален")
        return True
    else:
        print(f"Ошибка при удалении пользователя ID {user_id}: {res.status_code} - {res.text}")
        return False

def delete_sheet(session, sheet_id):
    """Удаление листа задач по ID"""
    url = DELETE_SHEET_URL.format(id=sheet_id)
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {"X-CSRFToken": csrf_token}
    
    res = session.delete(url, headers=headers)
    
    if res.status_code in [204, 200]:
        print(f"Лист задач ID {sheet_id} удален")
        return True
    else:
        print(f"Ошибка при удалении листа задач ID {sheet_id}: {res.status_code} - {res.text}")
        return False

def cleanup_test_data():
    """Очистка всех тестовых данных"""
    print("\n" + "="*50)
    print("ОЧИСТКА ТЕСТОВЫХ ДАННЫХ")
    print("="*50)
    
    try:
        # Входим под администратором для удаления данных
        admin_session = login("admin@example.com", "1")
        
        # Удаляем созданные листы задач
        if test_sheets:
            print("\nУдаление тестовых листов задач:")
            for sheet in test_sheets:
                delete_sheet(admin_session, sheet["id"])
        
        # Удаляем созданных пользователей (кроме администратора)
        if test_users:
            print("\nУдаление тестовых пользователей:")
            for user in test_users:
                delete_user(admin_session, user["id"])
        
        # Выходим из системы
        logout(admin_session)
        admin_session.close()
        
        print("\nОчистка завершена!")
        
    except Exception as e:
        print(f"Ошибка при очистке данных: {e}")

def run_integration_test():
    global test_sheets
    test_passed = False
    
    try:
        print("="*60)
        print("НАЧАЛО ИНТЕГРАЦИОННОГО ТЕСТА")
        print("="*60)
        
        print("-> Авторизация под админом (руководитель по умолчанию)...")
        admin_session = login("admin@example.com", "1")

        print("-> Получаем список ролей...")
        roles = get_roles(admin_session)
        role_head_id = roles.get("Manager")
        role_exec_id = roles.get("Executor")
        
        assert role_head_id is not None, "Роль Manager не найдена"
        assert role_exec_id is not None, "Роль Executor не найдена"

        print("-> Создаём руководителя...")
        head = register_user(admin_session, "TestHead", "head@example.com", "password123", "Начальник", role_head_id)

        print("-> Создаём исполнителя...")
        executor = register_user(admin_session, "TestExec", "exec@example.com", "password123", "Рабочий", role_exec_id)

        print("-> Выход из аккаунта админа...")
        logout(admin_session)

        print("-> Вход под исполнителем для проверки начального состояния...")
        exec_session = login("exec@example.com", "password123")
        sheets_before = get_executor_sheets(exec_session)
        print(f"Листов задач до: {len(sheets_before)}")
        assert len(sheets_before) == 0, "У нового исполнителя уже есть листы"
        exec_session.close()

        print("-> Вход под новым руководителем и создание листа задач...")
        head_session = login("head@example.com", "password123")

        sheet_payload = {
            "name": "Лист от руководителя",
            "user": head["id"],
            "tasks": [{
                "name": "Тестовая задача",
                "description": "Описание задачи",
                "date_start": "2025-06-13T00:00:00Z",
                "date_end": "2025-06-14T00:00:00Z",
                "user": executor["id"]
            }]
        }

        csrf_token = head_session.cookies.get("csrftoken", "")
        headers = {"X-CSRFToken": csrf_token}
        res = head_session.post(TASKSHEET_URL, json=sheet_payload, headers=headers)
        assert res.status_code == 201, f"Ошибка при создании листа задач: {res.text}"
        
        sheet_data = res.json()
        test_sheets.append(sheet_data)
        print("Лист задач успешно создан.")
        head_session.close()

        print("-> Повторная проверка у исполнителя...")
        exec_session = login("exec@example.com", "password123")
        sheets_after = get_executor_sheets(exec_session)
        print(f"Листов задач после: {len(sheets_after)}")
        for idx, sheet in enumerate(sheets_after, 1):
            print(f"    {idx}. {sheet.get('name', '<без названия>')}")

        assert len(sheets_after) == 1, "У исполнителя не появился лист задач"
        
        print("="*60)
        print("ИНТЕГРАЦИОННЫЙ ТЕСТ УСПЕШНО ПРОЙДЕН!")
        print("="*60)
        test_passed = True
        
    except Exception as e:
        print("="*60)
        print(f"ТЕСТ ПРОВАЛЕН: {e}")
        print("="*60)
        raise
    finally:
        # Всегда выполняем очистку
        cleanup_test_data()
        
    return test_passed

if __name__ == "__main__":
    try:
        success = run_integration_test()
        if success:
            sys.exit(0)  # Успех - exit code 0
        else:
            sys.exit(1)  # Провал - exit code 1
            
    except SystemExit:
        raise  # Передаем системный exit код дальше
        
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)  # Любая ошибка = exit code 1