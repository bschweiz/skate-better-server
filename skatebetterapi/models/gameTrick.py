
from django.db import models
from .trick import Trick

class GameTrick(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    trick = models.ForeignKey(Trick, on_delete=models.DO_NOTHING)
    user_make = models.BooleanField(default=True)
    opponent_make = models.BooleanField(default=True)
