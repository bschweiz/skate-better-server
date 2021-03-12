from django.db import models
from .trick import Trick
from .game import Game

class GameTrick(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    trick = models.ForeignKey(Trick, on_delete=models.DO_NOTHING)