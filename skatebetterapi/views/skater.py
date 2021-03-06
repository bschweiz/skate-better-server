
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

    
    def list(self, request):
        try:
            skater = Skater.objects.get(user=request.auth.user)
            skater.games = Game.objects.filter(skater=skater)

            profile = ProfileSerializer(skater, many=False, context={'context': request})

            return Response(profile.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('opponent', 'date_time', 'location', 'won')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    games = GameSerializer(many=True)

    class Meta:
        model = Skater
        fields = ('handle', 'goofy', 'fav_skater', 'fav_video', 'user', 'games')
