from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from django.utils import timezone

from application.models import User, Role, TaskSheet, Status, Task, Comment
from application.serializers import UserSerializer, UsersSerializer, RolesSerializer, ExecutorsSerializer, TaskSheetCreateSerializer, SheetsSerializer, TaskSheetUpdateSerializer, TaskSerializer, UsersSafeSerializer, CommentSerializer, StatusSerializer, SheetsExecutorSerializer

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from .permissions import IsManager


# class UserViewset(mixins.ListModelMixin, GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserViewset(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    # Упрощенный вход в систему
    @action(methods=["POST"], detail=False, url_path="login")
    def login_user(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response(
                {"success": False, "error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                "success": True,
                "username": user.username,
                "userId": user.id
            })
        else:
            return Response(
                {"success": False, "error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Получение информации о пользователе
    @action(methods=["GET"], detail=False, url_path="info")
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated,
        }
        
        if request.user.is_authenticated:
            role_name = None
            if request.user.role_id:  # Проверяем наличие role_id
                try:
                    # Получаем название роли из связанной модели Role
                    role_name = request.user.role.name
                except AttributeError:
                    # На случай если связь с Role не настроена
                    role_name = "Неизвестная роль"
            
            data.update({
                "username": request.user.username,
                "userId": request.user.id,
                "role_name": role_name
            })
        
        return Response(data)

    # Выход из системы
    @action(methods=["POST"], detail=False, url_path="logout")
    def logout_user(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"success": True, "message": "Successfully logged out."},
            status=status.HTTP_200_OK
        )

    # Защищенный метод (требует обычной аутентификации)
    @action(detail=False, methods=['GET'], url_path='protected', permission_classes=[IsAuthenticated])
    def protected_action(self, request, *args, **kwargs):
        return Response({
            "success": True,
            "message": "Access granted to protected action."
        })
class UsersViewset(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet, 
                      viewsets.ViewSet):
    permission_classes = [IsManager]
    serializer_class = UsersSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    queryset = User.objects.all()
    def list(self, request):
        users = User.objects.all()  # Получаем всех пользователей
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    
class RolesViewset(viewsets.ViewSet):
    def list(self, request):
        roles = Role.objects.all()  
        serializer = RolesSerializer(roles, many=True)
        return Response(serializer.data)
    
class StatusViewset(viewsets.ViewSet):
    def list(self, request):
        status = Status.objects.all()  
        serializer = StatusSerializer(status, many=True)
        return Response(serializer.data)
    
class UsersSafeViewset(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()  
        serializer = UsersSafeSerializer(users, many=True)
        return Response(serializer.data)
    
class ExecutorsViewset(viewsets.ViewSet):
    def list(self, request):
        # Получаем объект роли "Executor"
        executor_role = Role.objects.filter(name='Executor').first()
        
        if not executor_role:
            return Response({"error": "Role 'Executer' not found"}, status=404)
        
        # Фильтруем пользователей по роли
        executors = User.objects.filter(role=executor_role)
        
        serializer = ExecutorsSerializer(executors, many=True)
        return Response(serializer.data)
    
class TaskSheetCreateView(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet, 
                      viewsets.ViewSet):
    queryset = TaskSheet.objects.all()
    serializer_class = TaskSheetCreateSerializer

class TaskSheetViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = TaskSheet.objects.all()
    
    
    def get_serializer_class(self):
        
        if self.action in ['update', 'partial_update']:
            return TaskSheetUpdateSerializer
        return TaskSheetCreateSerializer  # Ваш существующий сериализатор
    
    @action(detail=True, methods=['patch'], url_path='confirm')
    def confirm(self, request, pk=None):
        sheet = self.get_object()
        sheet.confirmed = True
        sheet.save()
        return Response({'status': 'confirmed'})
    
    @action(detail=True, methods=['delete'])
    def purge(self, request, pk=None):
        """Полная очистка листа (удаление всех задач)"""
        sheet = self.get_object()
        sheet.task_set.all().delete()
        return Response({'status': 'purged'})
    
class SheetViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = SheetsSerializer

    def get_queryset(self):
        queryset = TaskSheet.objects.all()

        archived_param = self.request.query_params.get('archived')
        if archived_param is not None:
            if archived_param.lower() == 'true':
                queryset = queryset.filter(confirmed=True)
            elif archived_param.lower() == 'false':
                queryset = queryset.filter(confirmed=False)

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SheetsSerializer(queryset, many=True)
        return Response(serializer.data)
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return self.queryset.filter(sheet_id=self.kwargs['sheet_pk'])
    
    def perform_create(self, serializer):
        serializer.save(
            sheet_id=self.kwargs['sheet_pk'],
            status=Status.objects.get(name='Ожидание подтверждения')
        )



class CommentViewset(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(methods=["POST"], detail=False, url_path="write")
    def write_comment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Автоматически заполняем поля
        serializer.validated_data.update({
            'user': request.user,
            'date': timezone.now(),
            'read': False
        })
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False)
    def read(self, request):
        comment_id = request.query_params.get('id')
        if not comment_id:
            return Response(
                {"error": "Comment ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            comment = self.get_queryset().get(id=comment_id)
            if not comment.read:
                comment.read = True
                comment.save()
            return Response(CommentSerializer(comment).data)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
    @action(methods=["POST"], detail=False, url_path="mark-read")
    def mark_comments_read(self, request):
        task_id = request.data.get('task_id')

        if not task_id:
            return Response({"error": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем задачу
        task = Task.objects.get(id=task_id)


        comments = Comment.objects.filter(
                task_id=task_id,
                read=False
            ).exclude(user=request.user)

        # Обновляем их статус на прочитанные
        comments.update(read=True)

        return Response({"status": "Comments marked as read"}, status=status.HTTP_200_OK)
    @action(methods=["GET"], detail=False, url_path="check-unread-comments")
    def check_unread_comments(self, request):
        user = request.user
        role = user.role 

        if role == 'Executor':
            unread_comments = Comment.objects.filter(
                Q(read=False),
                Q(task__user=user),
                Q(task__sheet__confirmed=False),
                ~Q(user=user)
            )
        else:
            unread_comments = Comment.objects.filter(
                Q(read=False),
                Q(task__sheet__confirmed=False),
                ~Q(user=user)
            )  

        return Response({"has_unread": unread_comments.exists()})
    @action(methods=["GET"], detail=False, url_path="unread-sheets")
    def unread_sheets(self, request):
        user = request.user
        role = user.role

        # Получаем непрочитанные комментарии (не от самого пользователя)
        if role == 'Executor':
            unread_comments = Comment.objects.filter(
                Q(read=False),
                Q(task__user=user),
                Q(task__sheet__confirmed=False),
                ~Q(user=user)
            )
        else:  # Manager
            unread_comments = Comment.objects.filter(
                Q(read=False),
                Q(task__sheet__confirmed=False),
                ~Q(user=user)
            )

        # Достаём sheet_id через связи
        sheet_ids = unread_comments.values_list('task__sheet_id', flat=True).distinct()

        return Response({"sheet_ids": list(sheet_ids)})


        
class SheetExecutorViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = SheetsExecutorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем все листы, связанные с задачами пользователя и фильтруем по архивности
        user = self.request.user
        archived_param = self.request.query_params.get('archived')
        
        queryset = TaskSheet.objects.filter(task_set__user=user, confirmed=False).distinct()  # Фильтруем только активные листы

        # Фильтрация по архивности, если параметр передан
        if archived_param is not None:
            if archived_param.lower() == 'true':
                queryset = queryset.filter(confirmed=True)
            elif archived_param.lower() == 'false':
                queryset = queryset.filter(confirmed=False)

        return queryset

    def create(self, request, *args, **kwargs):
        # Запрещаем создание новых записей через POST
        return Response({"detail": "Method 'POST' is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        # Запрещаем обновление всех данных через PUT
        return Response({"detail": "Method 'PUT' is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()  # Получаем задачу
        status = request.data.get("status")
        
        if status:
            task.status = status
            task.save()
            return Response({"status": "Task status updated."}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
