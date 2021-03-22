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

        user_makes = GameTrick.objects.filter(
            game=self, user_make=True)
        opponent_makes = GameTrick.objects.filter(
            game=self, opponent_make=True)
        score = (user_makes - opponent_makes)

        return score.count()

    @property
    def opponent_score(self):

        opponent_makes = GameTrick.objects.filter(
            game=self, opponent_make=True)
        user_makes = GameTrick.objects.filter(
            game=self, user_make=True)
        score = (opponent_makes - user_makes)

        return score.count()

