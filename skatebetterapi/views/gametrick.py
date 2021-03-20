from skatebetterapi.views import game
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from skatebetterapi.models import Trick, GameTrick

class GameTricks(ViewSet):

    def create(self, request):
        
        gametrick = GameTrick()
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

    def list(self, request):
            try:
                gametricks = GameTrick.objects.all()

            # Support filtering by game id
                game = self.request.query_params.get('game', None)
                if game is not None:
                    gametricks = gametricks.filter(game=game)

                serializer = GameTrickSerializer(gametricks, many=True, context={'context': request})

                return Response(serializer.data)
                
            except Exception as ex:
                return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
            
class TrickSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trick
        fields = ('id','name', 'stance')

class GameTrickSerializer(serializers.ModelSerializer):
    """JSON serializer for game trick"""

    trick = TrickSerializer(many=False)
    class Meta:
        model = GameTrick

        fields = ('id', 'trick', 'game', 'user_make', 'opponent_make')