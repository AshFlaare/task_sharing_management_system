from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Role(models.Model):
    MANAGER = 1
    EXECUTOR = 2
    
    ROLE_CHOICES = (
        (MANAGER, 'Руководитель'),
        (EXECUTOR, 'Исполнитель'),
    )
    
    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    name = models.CharField(max_length=20, verbose_name="Название роли")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name

class User(AbstractUser):
    # Переопределяем стандартные поля
    username = models.CharField(
        _('ФИО'),
        max_length=150,
        help_text=_('Фамилия Имя Отчество')
    )
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _("Пользователь с таким email уже существует."),
        }
    )
    phone = models.CharField(_('Телефон'), max_length=20)
    position = models.CharField(_('Должность'), max_length=100)
    role = models.ForeignKey(
        'Role',
        on_delete=models.PROTECT,
        verbose_name=_('Роль'),
        null=True,
        blank=True
    )
    
    # Настройки аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'position']
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
    
    def __str__(self):
        return self.username
    
class Status(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название статуса")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name
    
class TaskSheet(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название листа")
    creation_date = models.DateTimeField(
        verbose_name="Дата и время создания",
        default=timezone.now,  # Автоматически устанавливает текущее время при создании
        editable=False  # Чтобы нельзя было изменить вручную через админку
    )
    confirmed = models.BooleanField(verbose_name="Завершено")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Руководитель',
        null=True
    )

    class Meta:
        verbose_name = "Лист задач"
        verbose_name_plural = "Листы задач"

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название задачи")
    description = models.CharField(max_length=250, verbose_name="Описание задачи")
    date_start = models.DateTimeField(verbose_name="Дата начала", default=timezone.now)
    date_end = models.DateTimeField(verbose_name="Дата окончания", default=timezone.now)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Выполняющий',
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        verbose_name='Статус',
        null=True
    )
    sheet = models.ForeignKey(
        TaskSheet,
        on_delete=models.SET_NULL,
        related_name='task_set',
        verbose_name='Лист задач',
        null=True
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.CharField(max_length=100, verbose_name="Текст комментария")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        null=True
    )
    date = models.DateTimeField(
        verbose_name="Дата и время создания",
        default=timezone.now,  # Автоматически устанавливает текущее время при создании
        editable=False  # Чтобы нельзя было изменить вручную через админку
    )
    read = models.BooleanField(
        verbose_name="Прочитано"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Задача',
        null=True
    )


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text

