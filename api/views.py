from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from .models import Card

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

    @action(detail=False)
    def me(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
