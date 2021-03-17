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
from skatebetterapi.models import Trick

class Tricks(ViewSet):
    
    def list(self, request):
        try:
            tricks = Trick.objects.all()
            
        

            serializer = TrickSerializer(tricks, many=True, context={'context': request})

            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)
        
class TrickSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trick
        fields = ('id','name', 'stance')
