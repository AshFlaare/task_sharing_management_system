from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from application.models import Status, Role, User

class Command(BaseCommand):
    help = 'Инициализирует БД: создает группы, суперпользователя, статусы и т.д.'

    def handle(self, *args, **options):
        self.stdout.write("Запуск полной инициализации БД...")

        # 1. Создание и применение миграций
        self.run_migrations()

        # 2. Инициализация данных
        self.create_roles()
        self.create_superuser()
        self.create_statuses()

        self.stdout.write(self.style.SUCCESS("Готово! БД полностью инициализирована."))

    def run_migrations(self):
        """Создает и применяет миграции."""
        self.stdout.write("Применение миграций...")
        try:
            call_command('makemigrations', interactive=False)
            call_command('migrate', interactive=False)
            self.stdout.write(self.style.SUCCESS("Миграции успешно применены."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка миграций: {e}"))
            raise

    def create_roles(self):
        """Создает базовые роли: Руководитель и Исполнитель"""
        roles_data = [
            {
                'id': Role.MANAGER,
                'name': 'Manager'
            },
            {
                'id': Role.EXECUTOR,
                'name': 'Executor'
            }
        ]
        
        created_count = 0
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                id=role_data['id'],
                defaults={'name': role_data['name']}
            )
            if created:
                self.stdout.write(f'Создана роль: {role.name} (ID={role.id})')
                created_count += 1
            else:
                self.stdout.write(f'Роль "{role.name}" уже существует')
        
        self.stdout.write(self.style.SUCCESS(f'Готово! Создано/найдено ролей: {created_count}/{len(roles_data)}'))

    def create_superuser(self):
        if not User.objects.filter(username='AshFlaare').exists():
            manager_role = Role.objects.get(id=Role.MANAGER)
            
            admin = User.objects.create_user(
                username='AshFlaare',
                email='admin@example.com',
                phone='+123456789',
                position='SuperUser',
                role=manager_role,
                password='1',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write('Суперпользователь "AshFlaare" создан.')
        else:
            self.stdout.write('Суперпользователь "AshFlaare" уже существует.')

    def create_statuses(self):
        """Создает стандартные статусы задач в системе"""
        statuses = [
            "Ожидание подтверждения",
            "Возникла проблема",
            "Запланировано",
            "На выполнении",
            "Задерживается",
            "Выполнено",
            "Не актуально"
        ]
        
        created_count = 0
        for status_name in statuses:
            status, created = Status.objects.get_or_create(
                name=status_name
            )
            if created:
                self.stdout.write(f'Создан статус: "{status.name}"')
                created_count += 1
            else:
                self.stdout.write(f'Статус "{status.name}" уже существует')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Готово! Создано/найдено статусов: {created_count}/{len(statuses)}'
            )
        )