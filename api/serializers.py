#from django.contrib.auth.models import User
from users.models import User
from .models import Card
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url', 
            'id',
            'username', 
            'birthday',
            'email',
            'bio',
        ]



class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = [
            'url', 
            'id',
            'creator',
            'title',
            'color',
            'font',
            'outer_text',
            'inner_text',
        ]