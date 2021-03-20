
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from skatebetterapi.models import Game, Trick, GameTrick

class GameTricks(ViewSet):

    def create(self, request):
        
        gametrick = GameTrick()
        game = Game.objects.latest('date_time')
        gametrick.game = game 
        trick = Trick.objects.get(pk=request.data['trickId'])
        gametrick.trick = trick 
        gametrick.user_make = request.data['userMake']
        gametrick.opponent_make = request.data['opponentMake']

        try:
            gametrick.save()
            serializer = GameTrickSerializer(gametrick, context={'request': request})
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