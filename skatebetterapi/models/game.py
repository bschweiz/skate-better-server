from django.db import models
from .skater import Skater
from .opponent import Opponent
from .gametrick import GameTrick


class Game(models.Model):

    skater = models.ForeignKey(Skater, on_delete=models.CASCADE)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    location = models.CharField(max_length=333)
    won = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now=True)

    @property
    def user_score(self):

        user_score = GameTrick.objects.filter(
            game=self, user_make=True)
        return user_score.count()

    @property
    def opponent_score(self):

        opponent_score = GameTrick.objects.filter(
            game=self, opponent_make=True)
        return opponent_score.count()

