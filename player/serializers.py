import random

from rest_framework import serializers

from player.models import Match, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "cpu")


class MatchSerializer(serializers.ModelSerializer):
    winner = PlayerSerializer(read_only=True)
    player1_choice = serializers.ChoiceField(choices=["ROCK", "PAPER", "SCISSORS"])
    player2_choice = serializers.ChoiceField(
        choices=["ROCK", "PAPER", "SCISSORS"], required=False, allow_null=True
    )

    class Meta:
        model = Match
        fields = ("player1", "player2", "player1_choice", "player2_choice", "winner")

    def to_internal_value(self, obj, *args, **kwargs):
        obj = super().to_internal_value(obj, *args, **kwargs)
        if obj.get("player2").cpu:
            obj["player2_choice"] = random.choice(["ROCK", "PAPER", "SCISSORS"])
        return obj
