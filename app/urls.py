"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter

from application.api import UserViewset, UsersViewset, RolesViewset, ExecutorsViewset, TaskSheetViewSet, SheetViewSet, TaskViewSet, UsersSafeViewset, CommentViewset, StatusViewset, SheetExecutorViewSet, AnalyticsViewSet
from django.urls import path, include

router = DefaultRouter()
# router.register("users", UserViewset, basename="users")
router.register("user", UserViewset, basename="user")
router.register("users", UsersViewset, basename="users")
router.register("userssafe", UsersSafeViewset, basename="userssafe")
router.register("roles", RolesViewset, basename="roles")
router.register("status", StatusViewset, basename="status")
router.register("executors", ExecutorsViewset, basename="executors")
router.register("task-sheets", TaskSheetViewSet, basename="task-sheets")



router.register("sheets", SheetViewSet, basename="sheets")

router.register("my-sheets/review", SheetExecutorViewSet, basename="sheets-executor")

router.register(r'sheet', TaskSheetViewSet, basename='sheet')
router.register(r'sheets/(?P<sheet_pk>\d+)/tasks', TaskViewSet, basename='task')

router.register(r'comment', CommentViewset, basename='comment')

router.register(r'analytics', AnalyticsViewSet, basename='analytics')





urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
]
