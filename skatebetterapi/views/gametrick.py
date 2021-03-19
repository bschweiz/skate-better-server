from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from skatebetterapi.models import GameTrick

class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for game trick"""
    class Meta:
        model = GameTrick
        
        fields = ('id', 'trick', 'name')