from django.db import models
from django.contrib.auth.models import AbstractUser

# Consider creating a custom user model from scratch as detailed at
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model


class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    followed_users = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers")

    def is_favorite_card(self, card_id):
        return self.favorite_cards.filter(id=card_id).count() == 1


