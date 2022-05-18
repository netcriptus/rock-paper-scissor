from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from xxlimited import new

from player.models import Match, Player, defeat_map
from player.serializers import MatchSerializer, PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        players = self.get_serializer(data=request.data, many=True)
        players.is_valid(raise_exception=True)
        self.perform_create(players)
        return JsonResponse({"players": players.data}, status=201)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny]


class ScoreViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        player1_name = request.query_params.get("player1")
        player2_name = request.query_params.get("player2")

        if player1_name is None or player2_name is None:
            return JsonResponse(
                {"error": "player1 and player2 are required"}, status=400
            )

        player1 = get_object_or_404(Player, name=player1_name)
        player2 = get_object_or_404(Player, name=player2_name)

        player1_score = Match.objects.filter(
            player1=player1, player2=player2, winner=player1
        ).count()
        player2_score = Match.objects.filter(
            player1=player1, player2=player2, winner=player2
        ).count()

        return JsonResponse({player1_name: player1_score, player2_name: player2_score})
