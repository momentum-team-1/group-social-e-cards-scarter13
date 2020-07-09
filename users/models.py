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
        """
        Custom method to be called on the current User to determine whether or not a particular Card is a favorite Card of that user.  This, in conjunction with the toggle_favorite_card view in views.py is used to allow an update to the Card instance and return a JSON response that can change the condition of the "favorite" button
        """
        return self.favorite_cards.filter(id=card_id).count() == 1


