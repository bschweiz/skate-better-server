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
from skatebetterapi.models import Skater, Game

class Skaters(ViewSet):
    # handle GET request to profile resource, returns JSON of User info and events
    # def list(self, request):
    #     skater = Skater.objects.get(user=request.auth.user)
    #     games = Game.objects.filter(games__skater=skater)

    #     games = GameSerializer(
    #         events, many=True, context={'request': request})
    #     skater = SkaterSerializer(
    #         skater, many=False, context={'request': request})
    #     # there is NO MODEL for Profile so we gotta make an obj fr. scatch
    #     profile = {}
    #     profile['skater'] = skater.data
    #     profile['games'] = games.data

    #     return Response(profile)

    
# gonna try and build a simple user data responder
    def list(self, request):
        try:
            skater = Skater.objects.get(user=request.auth.user)
            # games = Game.objects.filter(skater=skater)
            
            skater = SkaterSerializer( skater, many=False, context={'context': request})
            # games = GameSerializer(games, many=True, context={'context': request})

            profile = SkaterSerializer( skater, many=False, context={'context': request})

            return Response(profile.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_410_GONE)
        
class UserSerializer(serializers.ModelSerializer):
    # JSON serializer for gamer's related DJANGO 'User'
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class GameSerializer(serializers.ModelSerializer):
    # JSON serializer for gamer's related DJANGO 'User'
    class Meta:
        model = Game
        fields = ('opponent', 'date_time', 'location', 'won')

class SkaterSerializer(serializers.ModelSerializer):
    # JSON serilizer for Skaters
    user = UserSerializer(many=False)
    games = GameSerializer(many=True)

    class Meta:
        model = Skater
        fields = ('handle','goofy', 'fav_skater', 'fav_video', 'user')
