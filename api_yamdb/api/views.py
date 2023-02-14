from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
# Create your views here.
from django.shortcuts import get_object_or_404
from users.models import User

from api.serialisers import (
    UserSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователем"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignUpViewSet(viewsets.ModelViewSet):
    """Класс регистрации и выдачи подтверждения пользователю на почту"""

    pass
    # queryset = User.objects.all()
