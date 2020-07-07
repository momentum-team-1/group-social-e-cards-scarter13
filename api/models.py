from django.db import models
from users.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Card(models.Model):
    COLOR_ONE = 'C_ONE'
    COLOR_TWO = 'C_TWO'
    #COLOR_THREE = 'C_THREE'
    #COLOR_FOUR = 'C_FOUR'
    #COLOR_FIVE = 'C_FIVE'
    #COLOR_SIX = 'C_SIX'
    #COLOR_SEVEN = 'C_SEVEN'
    #COLOR_EIGHT = 'C_EIGHT'
    COLOR_CHOICES =[
        (COLOR_ONE, 'Color 1'),
        (COLOR_TWO, 'Color 2'),
        #(COLOR_THREE, 'Color 3'),
        #(COLOR_FOUR, 'Color 4'),
        #(COLOR_FIVE, 'Color 5'),
        #(COLOR_SIX, 'Color 6'),
        #(COLOR_SEVEN, 'Color 7'),
        #(COLOR_EIGHT, 'Color 8'),
    ]
    FONT_ONE = 'F_ONE'
    FONT_TWO = 'F_TWO'
    #FONT_THREE = 'F_THREE'
    #FONT_FOUR = 'F_FOUR'
    #FONT_FIVE = 'F_FIVE'
    #FONT_SIX = 'F_SIX'
    #FONT_SEVEN = 'F_SEVEN'
    #FONT_EIGHT = 'F_EIGHT'
    FONT_CHOICES =[
        (FONT_ONE, 'Font 1'),
        (FONT_TWO, 'Font 2'),
        #(FONT_THREE, 'Font 3'),
        #(FONT_FOUR, 'Font 4'),
        #(FONT_FIVE, 'Font 5'),
        #(FONT_SIX, 'Font 6'),
        #(FONT_SEVEN, 'Font 7'),
        #(FONT_EIGHT, 'Font 8'),
    ]
    creator = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=25, choices=COLOR_CHOICES, default=COLOR_ONE)
    font = models.CharField(max_length=25, choices=FONT_CHOICES, default=FONT_ONE)
    outer_text = models.TextField(blank=True, null=True)
    inner_text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    favorite_of = models.ManyToManyField(to=User, blank=True, related_name="favorite_cards")

    class Meta:
        ordering = ['-date']

    
