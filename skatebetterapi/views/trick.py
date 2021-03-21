
import sqlite3
import json

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

            serializer = TrickSerializer(
                tricks, many=True, context={'context': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def available(self, request, pk=None):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            try:
                db_cursor.execute("""
                    SELECT t.id, t.name
                            FROM skatebetterapi_trick AS t
                            WHERE t.id NOT IN 

                            (SELECT t.id
                                FROM skatebetterapi_gametrick AS gt
                                JOIN skatebetterapi_game AS g
                                ON gt.game_id = g.id
                                JOIN skatebetterapi_trick AS t
                                ON gt.trick_id = t.id
                                WHERE gt.game_id = 1) 
                    """)
                availableTricks = []
                dataset = db_cursor
                
                for row in dataset:

                    # Create an trick instance from the current row
                    trickId = row['id']


                    availableTricks.append(trickId)

                return Response(availableTricks)

            except Exception as ex:
                return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)


class TrickSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trick
        fields = ('id', 'name', 'stance')
