# from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets

from .serializers import UserModelSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserModelSerializer


