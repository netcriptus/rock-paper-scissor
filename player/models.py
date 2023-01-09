from django.db import models

playable_choices = (("ROCK", "rock"), ("PAPER", "raper"), ("SCISSORS", "rcissors"))

defeat_map = {"ROCK": "SCISSORS", "PAPER": "ROCK", "SCISSORS": "PAPER"}


class Player(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    cpu = models.BooleanField(default=False)


class Match(models.Model):
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player1"
    )
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player2"
    )
    player1_choice = models.CharField(max_length=10, choices=playable_choices)
    player2_choice = models.CharField(max_length=10, choices=playable_choices)
    winner = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="winner", blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.player1_choice == self.player2_choice:
            self.winner = None
        elif self.player1_choice == defeat_map[self.player2_choice]:
            self.winner = self.player2
        elif self.player2_choice == defeat_map[self.player1_choice]:
            self.winner = self.player1
