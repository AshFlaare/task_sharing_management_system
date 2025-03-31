from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from application.models import User


# Create your views here.
# class UserListView(ApiView):
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
    
#     def get_queryset(self):
#         user = self.request.user
#         return super().get_queryset()