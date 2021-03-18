
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from skatebetterapi.models import Skater, Game, Opponent, opponent

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

    @action(methods=['post'], detail=False)
    def addnewopponent(self, request, pk=None):
        # when you need to add an opponent and a new game
        opponent = Opponent()
        opponent.skater = Skater.objects.get(user=request.auth.user)
        opponent.handle = request.data['handle']
        opponent.goofy = request.data['goofy']
        opponent.save()

        game = Game()
        skater = Skater.objects.get(user=request.auth.user)
        game.opponent = Opponent.objects.get(handle=request.data['handle'])
        game.skater = skater
        game.opponent_id = opponent.id
        game.location = request.data['location']
        

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class OpponentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Opponent
        fields = ('handle', 'goofy')

class GameSerializer(serializers.ModelSerializer):
    opponent = OpponentSerializer(many=False)
    
    class Meta:
        model = Game
        fields = ('opponent', 'won', 'date_time', 'location')
