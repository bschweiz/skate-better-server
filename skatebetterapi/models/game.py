from django.db import models
from .skater import Skater
from .opponent import Opponent

class Game(models.Model):

    skater = models.ForeignKey(Skater, on_delete=models.CASCADE)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    location = models.CharField(max_length=333)
    won = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now=True)

    @property
    def number_sold(self):
        """number_sold property of a product
        Returns:
            int -- Number items on completed orders
        """
        sold = OrderProduct.objects.filter(
            product=self, order__payment_type__isnull=False)
        return sold.count()

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