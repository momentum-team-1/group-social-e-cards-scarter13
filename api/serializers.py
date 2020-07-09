#from django.contrib.auth.models import User
from users.models import User
from .models import Card
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'birthday',
            'email',
            'bio',
        ]

#class FavoriteCardField(serializers.RelatedField):
#    def to_representation(self, value):
#        if self.favorite_of == request.user:
#            is_favorite = True
#        else:
#            is_favorite = False
#
#        return is_favorite


class CardSerializer(serializers.ModelSerializer):
    #is_favorite = FavoriteCardField(queryset=Card.objects.all(), many=False)

    class Meta:
        model = Card
        fields = [ 
            'id',
            'creator',
            'title',
            'color',
            'font',
            'outer_text',
            'inner_text',
            'favorite_of',
        ]

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'id',
        ]