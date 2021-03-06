from django.db import models
from .skater import Skater
from .opponent import Opponent
from .gametrick import GameTrick


class Game(models.Model):

    skater = models.ForeignKey(Skater, on_delete=models.CASCADE)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    location = models.CharField(max_length=333)
    date_time = models.DateTimeField(auto_now=True)

    @property
    def user_score(self):
        try:  
            user_points = (GameTrick.objects.filter(
                game=self, user_make=True, opponent_make=False)).count()
            return user_points

        except: 
            user_points = 0
            return user_points
        

    @property
    def opponent_score(self):
        try:
            opponent_points = (GameTrick.objects.filter(
                game=self, user_make=False, opponent_make=True)).count()
            return opponent_points
        
        except: 
            opponent_points = 0
            return opponent_points

    @property
    def won(self):
        try:
            won = True if (self.user_score > self.opponent_score) else  False
            return won
        except: 
            won = False
            return won

