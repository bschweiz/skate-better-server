# from levelupapi.views.game import GameSerializer
# from levelupapi.views.event import EventSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from skatebetterapi.models import Skater, Game, Opponent

class Opponents(ViewSet):
   
    
# gonna try and build a simple user data responder
    def list(self, request):
        try:
            skater = Skater.objects.get(user=request.auth.user)
            opponent = Opponent.objects.filter(skater=skater)
            
        
            # games = GameSerializer(games, many=True, context={'context': request})
            skater.games = Game.objects.filter(skater=skater)

            opponent = OpponentSerializer(opponent, many=True, context={'context': request})

            return Response(profile.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
        
class OpponentSerializer(serializers.ModelSerializer):
    # JSON serializer for gamer's related DJANGO 'User'
    class Meta:
        model = Opponent
        fields = ('handle', 'goofy')

class GameSerializer(serializers.ModelSerializer):
    # JSON serializer for gamer's related DJANGO 'User'
    class Meta:
        model = Game
        fields = ('opponent', 'date_time', 'location', 'won')

class ProfileSerializer(serializers.ModelSerializer):
    # JSON serilizer for Skaters
    user = UserSerializer(many=False)
    games = GameSerializer(many=True)

    class Meta:
        model = Skater
        fields = ('handle','goofy', 'fav_skater', 'fav_video', 'user', 'games')
