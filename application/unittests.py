from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Role, Status, TaskSheet, Task, Comment

User = get_user_model()

class ModelCreationTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(id=1, name='Руководитель')
        self.status = Status.objects.create(name='В процессе')

        self.user = User.objects.create_user(
            username='Иванов Иван Иванович',
            email='ivan@example.com',
            password='password123',
            phone='+79990000000',
            position='Начальник отдела',
            role=self.role
        )

        self.sheet = TaskSheet.objects.create(
            name='Тестовый лист',
            confirmed=False,
            user=self.user
        )

        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание задачи',
            date_start=timezone.now(),
            date_end=timezone.now(),
            user=self.user,
            status=self.status,
            sheet=self.sheet
        )

        self.comment = Comment.objects.create(
            text='Комментарий к задаче',
            user=self.user,
            read=False,
            task=self.task
        )

    def test_role_creation(self):
        self.assertEqual(str(self.role), 'Руководитель')

    def test_user_creation(self):
        self.assertEqual(str(self.user), 'Иванов Иван Иванович')
        self.assertEqual(self.user.email, 'ivan@example.com')
        self.assertEqual(self.user.role, self.role)

    def test_status_creation(self):
        self.assertEqual(str(self.status), 'В процессе')

    def test_tasksheet_creation(self):
        self.assertEqual(str(self.sheet), 'Тестовый лист')
        self.assertEqual(self.sheet.user, self.user)

    def test_task_creation(self):
        self.assertEqual(str(self.task), 'Тестовая задача')
        self.assertEqual(self.task.sheet, self.sheet)
        self.assertEqual(self.task.status, self.status)

    def test_comment_creation(self):
        self.assertEqual(str(self.comment), 'Комментарий к задаче')
        self.assertEqual(self.comment.task, self.task)
        self.assertFalse(self.comment.read)
