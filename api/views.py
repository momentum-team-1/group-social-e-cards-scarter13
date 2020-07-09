from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .models import Card
from .serializers import UserSerializer, CardSerializer, FriendSerializer



class UserViewSet(viewsets.ModelViewSet):
    """
    Allows admin-level access to Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        """
        Custom perform_create method that will attach the request.user to the card as the 'creator' once the card is saved
        """
        serializer.save(creator=self.request.user)


    def destroy(self, request, pk):
        """
        Custom destroy method to limit card deletion to card creators
        """
        instance = self.get_object()
        if instance.creator == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("This Card does not belong to you", status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, permission_classes = [permissions.IsAuthenticated])
    """
    Return a list of cards that have been created by the request.user
    """
    def me(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)


    @action(detail=False, permission_classes = [permissions.IsAuthenticated])
    """
    Return a list of all cards from all users while maintaining the default pagination settings
    """
    def all(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, permission_classes = [permissions.IsAuthenticated])
    """
    Return a list of cards from users followed by the request.user
    """
    def friends(self, request):
        cards = Card.objects.filter(creator__followers = request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)


class FollowedUserView(GenericAPIView):
    """
    Show limited user data belonging to users that are being followed by the request.user
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]  
    serializer_class = FriendSerializer


    def get(self, request, format=None):
        """
        Custom GET method that will return a list of users that are followed by the request.user
        """
        my_followed_users = User.objects.filter(followers=request.user)
        serializer = self.get_serializer(my_followed_users, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """
        Custom POST method that will add a user to the request.user's list of followed users
        """
        name_of_user = request.data["user"]
        user_to_follow = User.objects.get(username=name_of_user)
        current_user = request.user
        current_user.followed_users.add(user_to_follow)
        return Response("User Added!", status=status.HTTP_200_OK)

        
class DeleteFollowedUser(APIView):
    """
    Remove a user from the request.user's list of followed users.  This view exists seperately from the GenericAPIView above to allow for an altered path in URLs
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id, format=None):  
        user_to_remove = get_object_or_404(User, id=user_id)
        current_user = request.user
        current_user.followed_users.remove(user_to_remove)
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteCardsView(GenericAPIView):
    """
    Used to return cards that have been favorited by the request.user
    """
    queryset = Card.objects.all()
    permission_classes = [permissions.IsAuthenticated]  
    serializer_class = CardSerializer


    def get(self, request, format=None):
        """
        Custom GET method to return a list of cards that have been favorited by the request.user
        """
        my_favorite_cards = Card.objects.filter(favorite_of=request.user)
        serializer = self.get_serializer(my_favorite_cards, many=True)
        return Response(serializer.data)
        

#    def post(self, request, format=None):
        """
        The original attempt to add a card to the request.user's list of favorites.  A custom "POST" method to interpret incoming JSON data and apply it to the card instance.  After considering that a custom DELETE method would also be required, and knowing that we wanted this function to work with the click of an event listener, I decided that it would be easier to use a toggle method instead, allowing the URL to be the same for "favoriting" and "unfavoriting" from the front end.  
        """
#        """Add a Card to your list of favorite cards"""
#        card_id = request.data["id"]
#        new_favorite_card = Card.objects.get(id=card_id)
#        current_user = request.user
#        new_favorite_card.favorite_of.add(current_user)
#        return Response("Card added to favorites!", status=status.HTTP_200_OK)

def toggle_favorite_card(request, card_id, permission_classes = [permissions.IsAuthenticated]):
    """
    Function to toggle a specific card between being favorited or not.  Works in conjunction with the custom method 'is_favorite_card' on the User model.
    """
    card = get_object_or_404(Card, id=card_id)

    if request.user.is_favorite_card(card_id):
        request.user.favorite_cards.remove(card)
        return JsonResponse({"isFavorite": False})
    else:
        request.user.favorite_cards.add(card)
        return JsonResponse({"isFavorite": True})