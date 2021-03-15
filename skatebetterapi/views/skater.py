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
    def list(self, request):
        skater = Skater.objects.get(user=request.auth.user)
        games = Game.objects.filter(eventgamer__gamer=gamer)

        games = GameSerializer(
            events, many=True, context={'request': request})
        skater = SkaterSerializer(
            gamer, many=False, context={'request': request})
        # there is NO MODEL for Profile so we gotta make an obj fr. scatch
        profile = {}
        profile['skater'] = skater.data
        profile['games'] = games.data

        return Response(profile)

    
# gonna try and build a simple user data responder
    def retrieve(self, request, pk=None)
        try:
            skater = Skater.objects.get(user=request.auth.user)

        
class UserSerializer(serializers.ModelSerializer):
    # JSON serializer for gamer's related DJANGO 'User'
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class SkaterSerializer(serializers.ModelSerializer):
    # JSON serilizer for Skaters
    user = UserSerializer(many=False)

    class Meta:
        model = Skater
        fields = ('first_name', 'last_name', 'username', 'goofy', 'fav_skater', 'fav_video')
