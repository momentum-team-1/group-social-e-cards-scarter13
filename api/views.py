from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .models import Card
from .serializers import UserSerializer, CardSerializer, FriendSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    #def get_queryset(self):
    #    current_user=self.request.user
    #    queryset = Card.objects.filter(creator__followers = current_user)
    #    return queryset

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

class FollowedUserView(GenericAPIView):
    """
    Show friends that are being followed by the request.user
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]  
    serializer_class = FriendSerializer
    def get(self, request, format=None):
        my_followed_users = User.objects.filter(followers=request.user)
        serializer = self.get_serializer(my_followed_users, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """Add a User to your list of followed users"""
        name_of_user = request.data["user"]
        user_to_follow = User.objects.get(username=name_of_user)
        current_user = request.user
        current_user.followed_users.add(user_to_follow)
        return Response("User Added!", status=status.HTTP_200_OK)

        
class DeleteFollowedUser(APIView):
    """Remove a user from your list of followed users"""
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, user_id, format=None):  
        user_to_remove = get_object_or_404(User, id=user_id)
        current_user = request.user
        current_user.followed_users.remove(user_to_remove)
        return Response(status=status.HTTP_204_NO_CONTENT)
