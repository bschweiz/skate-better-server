from django.db import models
from .skater import Skater
from .gametype import GameType

class Trick(models.Model):

    skater = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game_type = models.ForeignKey("GameType", on_delete= models.CASCADE)
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=333)