from django.shortcuts import render
from rest_framework.decorators import action
from users.models import User
from .models import Card
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, CardSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)