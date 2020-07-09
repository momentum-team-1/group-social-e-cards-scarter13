from django.db import models
from users.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

"""
Create a token for each new user
"""
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Card(models.Model):
    creator = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=25, default="C_ONE")    
    font = models.CharField(max_length=25, default="F_ONE")    
    outer_text = models.TextField(blank=True, null=True)
    inner_text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    favorite_of = models.ManyToManyField(to=User, blank=True, related_name="favorite_cards")

    class Meta:
        ordering = ['-date']


