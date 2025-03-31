from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from application.models import User
from application.serializers import UserSerializer


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer

# class UserViewset(mixins.ListModelMixin, GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewset(GenericViewSet):
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