from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
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

    @action(detail=False, permission_classes = [permissions.IsAuthenticated])
    def me(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes = [permissions.IsAuthenticated])
    def all(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

class FollowedUserView(APIView):
    """
    Show friends that are being followed by the request.user ... or is it better to make this add a friend?
    """
    authentication_classes = [authentication.TokenAuthentication]
    def get(self, request, format=None):
        my_followed_users = User.objects.filter(self__in=objects.followers)

        return Response(my_followed_users)


#    def post(self, request, format=None):
#        name_of_user = request.data["user"]
#        user = User.objects.get(username=name_of_user)
#        current_user = request.user
#        current_user.followed_users.add(user_to_follow)
#        return Response(
#            {followed_user}
#        )
        
    
