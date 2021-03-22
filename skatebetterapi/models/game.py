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
            product=self, order__payment_type__isnull=False)
        return user_score.count()
    
    @property
    def opponent_score(self):
        
        opponent_score = GameTrick.objects.filter(
            product=self, order__payment_type__isnull=False)
        return opponent_score.count()

    @property
    def can_be_rated(self):
        """can_be_rated property, which will be calculated per user
        Returns:
            boolean -- If the user can rate the product or not
        """
        return self.__can_be_rated

    @can_be_rated.setter
    def can_be_rated(self, value):
        self.__can_be_rated = value

    @property
    def average_rating(self):
        """Average rating calculated attribute for each product
        Returns:
            number -- The average rating for the product
        """
        ratings = ProductRating.objects.filter(product=self)
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        try: 
            avg = total_rating / len(ratings)
        except: 
            ZeroDivisionError 
            avg = "No ratings yet." 
        return avg