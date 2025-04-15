from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from application.models import User, Role, Task, TaskSheet, Status, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role_id']
        
    
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email', 'phone', 'position', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,  # Не обязателен при обновлении
                'allow_blank': True  # Разрешаем пустую строку
            }
        }

    def create(self, validated_data):
        # Хэшируем пароль при создании
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Хэшируем пароль только если он был предоставлен
        if 'password' in validated_data and validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
        elif 'password' in validated_data:
            # Если пароль пустой - удаляем его из validated_data
            del validated_data['password']
        
        return super().update(instance, validated_data)
    
class UsersSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class ExecutorsSerializer(serializers.ModelSerializer):
    active_tasks_count = serializers.SerializerMethodField()
    all_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'position', 'active_tasks_count', 'all_tasks_count']

    def get_active_tasks_count(self, obj):
        """Количество активных задач (текущая дата между date_start и date_end)"""
        now = timezone.now()
        return Task.objects.filter(
            user=obj,
            date_start__lte=now,
            date_end__gte=now
        ).count()

    def get_all_tasks_count(self, obj):
        """Общее количество задач, назначенных пользователю"""
        return Task.objects.filter(user=obj).count()

class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date_start', 'date_end', 'status']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    date = serializers.DateTimeField(
        read_only=True,
        default=timezone.now
    )
    read = serializers.BooleanField(
        read_only=True,
        default=False
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'date', 'read', 'task']
        read_only_fields = ['id', 'user', 'date', 'read']  # Все неизменяемые поля
        extra_kwargs = {
            'text': {
                'required': True,
                'allow_blank': False,
                'max_length': 1000
            },
            'task': {
                'required': True
            }
        }

    def validate_text(self, value):
        """Кастомная валидация текста комментария"""
        if not value.strip():
            raise serializers.ValidationError("Текст комментария не может быть пустым")
        return value

class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # Добавляем комментарии
    
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'date_start', 'date_end', 
                'user', 'status', 'sheet', 'comments']  # Добавляем 'comments' в fields
        extra_kwargs = {
            'sheet': {'read_only': True},
            # 'status': {'read_only': True},
            # 'description': {'required': False}  # Раскомментируйте если нужно сделать необязательным
        }
    


class TaskSheetCreateSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, write_only=True)
    
    class Meta:
        model = TaskSheet
        fields = ['id', 'name', 'confirmed', 'user', 'tasks']
        extra_kwargs = {
            'confirmed': {'default': False},
            'user': {'required': True}
        }

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks')
        waiting_status = Status.objects.get(name='Ожидание подтверждения')
        
        task_sheet = TaskSheet.objects.create(**validated_data)
        
        tasks = [
            Task(
                sheet=task_sheet,
                status=waiting_status,
                **task_data
            )
            for task_data in tasks_data
        ]
        Task.objects.bulk_create(tasks)
        
        return task_sheet

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tasks'] = TaskSerializer(
            instance.task_set.all(),
            many=True
        ).data
        return representation

class SheetsSerializer(serializers.ModelSerializer):
    total_status = serializers.SerializerMethodField()

    class Meta:
        model = TaskSheet
        fields = ['id', 'name', 'confirmed', 'user', 'creation_date', 'total_status']

    def get_total_status(self, obj):
        statuses = [
            "Возникла проблема",          
            "Задерживается",              
            "Ожидание подтверждения",     
            "На выполнении",              
            "Запланировано",              
            "Выполнено",                  
            "Не актуально",               
        ]
        status_priority = {status: i for i, status in enumerate(statuses)}
        tasks = obj.task_set.all()
        if not tasks.exists():
            return "Нет задач"

        sorted_tasks = sorted(tasks, key=lambda t: status_priority.get(str(t.status), 100))
        return str(sorted_tasks[0].status)



class TaskSheetUpdateSerializer(serializers.ModelSerializer):
    tasks = serializers.ListField(
        child=TaskSerializer(),  # Теперь включает комментарии в выводе
        #write_only=True,
        required=False,
    )
    
    class Meta:
        model = TaskSheet
        fields = ['id', 'name', 'confirmed', 'user', 'tasks']
        extra_kwargs = {
            'user': {'read_only': True},
            'confirmed': {'read_only': True}
        }

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', None)
        instance = super().update(instance, validated_data)
        
        if tasks_data is not None:
            self._update_tasks(instance, tasks_data)
        
        return instance

    def _update_tasks(self, sheet, tasks_data):
        existing_tasks = {task.id: task for task in sheet.task_set.all()}
        updated_ids = []
        
        for task_data in tasks_data:
            task_id = task_data.get('id')
            
            if task_id and task_id in existing_tasks:
                task = existing_tasks[task_id]
                for field, value in task_data.items():
                    setattr(task, field, value)
                task.save()
                updated_ids.append(task_id)
            elif not task_id:
                Task.objects.create(
                    sheet=sheet,
                    status=Status.objects.get(name='Ожидание подтверждения'),
                    **task_data
                )
        
        sheet.task_set.exclude(id__in=updated_ids).delete()

class TaskSheetReadSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)  # Включаем задачи с комментариями
    
    class Meta:
        model = TaskSheet
        fields = ['id', 'name', 'confirmed', 'user', 'tasks']
        extra_kwargs = {
            'user': {'read_only': True},
            'confirmed': {'read_only': True}
        }

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']

class ConfirmSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSheet
        fields = ['confirmed']

    def update(self, instance, validated_data):
        instance.confirmed = validated_data.get('confirmed', instance.confirmed)
        instance.save()
        return instance
    
class SheetsExecutorSerializer(serializers.ModelSerializer):
    total_status = serializers.SerializerMethodField()

    class Meta:
        model = TaskSheet
        fields = ['id', 'name', 'confirmed', 'user', 'creation_date', 'total_status']

    def get_total_status(self, obj):
        statuses = [
            "Возникла проблема",          
            "Задерживается",              
            "Ожидание подтверждения",     
            "На выполнении",             
            "Запланировано",             
            "Выполнено",                 
            "Не актуально",              
        ]
        status_priority = {status: i for i, status in enumerate(statuses)}
        tasks = obj.task_set.all()

        if not tasks.exists():
            return "Нет задач"

        # Сортируем задачи по приоритету статуса
        sorted_tasks = sorted(tasks, key=lambda t: status_priority.get(str(t.status), 100))
        
        # Возвращаем статус задачи с наивысшим приоритетом
        return str(sorted_tasks[0].status)
    


