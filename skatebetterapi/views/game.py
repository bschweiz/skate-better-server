
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
        game.location = request.data['location']
        game.skater = skater
        game.opponent = opponent


        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        @api {GET} /game/:id GET product
        @apiName GetGame
        @apiGroup Game
        @apiParam {id} id Game Id
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            skater = Skater.objects.get(user=request.auth.user)
            games = Game.objects.filter(skater_id=skater.id)

            serializer = GameSerializer(games, many=True, context={'context': request})

            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request):
        
        game = Game()
        skater = Skater.objects.get(user=request.auth.user)
        opponent = Opponent.objects.get(pk=request.data['opponentId'])
        game.skater = skater
        game.opponent = opponent
        game.location = request.data['location']
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /products/:id DELETE product
        @apiName DeleteProduct
        @apiGroup Product
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Product Id to delete
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    
    @action(methods=['post'], detail=False)
    def rematch(self, request, pk=None):
        # when you need to rematch the same opponent at same

        game = Game()
        original_game = Game.objects.latest('date_time')
        skater = Skater.objects.get(user=request.auth.user)
        game.skater = skater
        game.opponent = original_game.opponent
        game.location = original_game.location
        

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def current(self, request, pk=None):

        game = Game.objects.latest('date_time')
        
        try:

            serializer = GameSerializer(game, many=False, context={'context': request})

            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

class OpponentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Opponent
        fields = ('handle', 'id', )

class GameSerializer(serializers.ModelSerializer):
    opponent = OpponentSerializer(many=False)
    
    class Meta:
        model = Game
        fields = ('opponent', 'won', 'date_time', 'location', 'id', 'user_score', 'opponent_score', )
