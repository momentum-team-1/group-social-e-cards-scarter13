from django.shortcuts import render
#from django.contrib.auth.models import User
from users.models import User
from .models import Card
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, CardSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AllCardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]