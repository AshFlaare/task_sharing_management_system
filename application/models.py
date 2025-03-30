from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Role(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=20, db_collation='Cyrillic_General_CI_AS', verbose_name="Название роли")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self) -> str:
        return self.name

class User(AbstractUser):
    # Основные поля
    last_name = models.CharField(_('Фамилия'), max_length=150)  # Оставляем для ФИО
    first_name = models.CharField(_('Имя'), max_length=150)     # Оставляем для ФИО
    patronymic = models.CharField(_('Отчество'), max_length=150, blank=True)  # Добавляем отчество
    email = models.EmailField(_('Email'), unique=True)          # Делаем email обязательным и уникальным
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    position = models.CharField(_('Должность'), max_length=100, blank=True)
    role = models.ForeignKey(
        'Role', 
        on_delete=models.PROTECT, 
        verbose_name=_('Роль'),
        null=False  # Убираем null, если роль обязательна
    )
    
    # Настройки аутентификации
    username = None  # Отключаем стандартное поле username
    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Обязательные поля при создании пользователя
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Возвращает полное ФИО"""
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
    
    def get_short_name(self):
        """Возвращает краткое имя (Фамилия И.О.)"""
        patronymic_initial = f"{self.patronymic[0]}." if self.patronymic else ""
        return f"{self.last_name} {self.first_name[0]}.{patronymic_initial}"
    
    @property
    def is_manager(self):
        return self.role_id == Role.MANAGER
    
    @property
    def is_executor(self):
        return self.role_id == Role.EXECUTOR
    
