
import sqlite3
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from skatebetterapi.models import Trick, Game


class Tricks(ViewSet):

    def list(self, request):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            tricks = Trick.objects.all()

            try:
# Support filtering available tricks by game id
                gameId = self.request.query_params.get('gameId', None)

                if gameId is not None:

                    game = Game.objects.get(pk=gameId)
                    currentGameId = game.id

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
                                WHERE gt.game_id = ?)
                                """, (gameId, ))

                    availableTricks = []
                    dataset = db_cursor

                    for row in dataset:
                        trickId = row['id']

                        trick = Trick.objects.get(pk=trickId)
                        availableTricks.append(trick)

                        serializer = TrickSerializer(
                            availableTricks, many=True, context={'context': request})

                    return Response(serializer.data)

            except Exception as ex:
                return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def available(self, request, pk=None):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            try:
                game = Game.objects.latest('date_time')
                currentGameId = game.id
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
                                WHERE gt.game_id = ?) 
                                """, (currentGameId, ))

                availableTricks = []
                dataset = db_cursor

                for row in dataset:
                    trickId = row['id']

                    trick = Trick.objects.get(pk=trickId)
                    availableTricks.append(trick)

                    serializer = TrickSerializer(
                        availableTricks, many=True, context={'context': request})

                return Response(serializer.data)

            except Exception as ex:
                return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)


class TrickSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trick
        fields = ('id', 'name', 'stance')
