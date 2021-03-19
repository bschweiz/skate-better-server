from skatebetterapi.views import game
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from skatebetterapi.models import Trick, GameTrick, gametrick

def list(self, request):
        try:
            gametrick = GameTrick.objects.all()
            gametrick.trick = Trick.objects.get(trick=trick)

            serializer = GameTrickSerializer(gametrick, many=True, context={'context': request})

            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
        
class TrickSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trick
        fields = ('id','name', 'stance')

class GameTrickSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for game trick"""

    trick = TrickSerializer(many=False)
    class Meta:
        model = GameTrick

        fields = ('id', 'trick', 'game', 'user_make', 'opponent_make')