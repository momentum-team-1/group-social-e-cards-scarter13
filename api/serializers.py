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



class CardSerializer(serializers.ModelSerializer):
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
        ]

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'id',
        ]