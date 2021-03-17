
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from skatebetterapi.models import Skater, Game, Opponent

class Games(ViewSet):

    def create(self, request):
        
        game = Game()
        skater = Skater.objects.get(user=request.auth.user)
        opponent = Opponent.objects.get(pk=request.data['opponentId'])
        game.skater = skater
        game.opponent = opponent
        game.location = request.data['location']

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request):
        
        game = Game()
        skater = Skater.objects.get(user=request.auth.user)
        opponent = Opponent.objects.get(pk=request.data['opponentId'])
        game.skater = skater
        game.opponent = opponent
        game.location = request.data['location']
        game.won = request.data['won']
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request):
        try:
            skater = Skater.objects.get(user=request.auth.user)
            games = Game.objects.filter(skater=skater)
            
        

            serializer = GameSerializer(games, many=True, context={'context': request})

            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
        
class OpponentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Opponent
        fields = ('handle', 'goofy')

class GameSerializer(serializers.ModelSerializer):
    opponent = OpponentSerializer(many=False)
    
    class Meta:
        model = Game
        fields = ('opponent','won', 'date_time', 'location')
