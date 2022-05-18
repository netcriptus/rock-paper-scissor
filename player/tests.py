from django.test import Client, TestCase

from player.models import Match, Player


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def post(self, url, data):
        return self.client.post(url, data=data, content_type="application/json")

    def get(self, url, *args, **kwargs):
        return self.client.get(url, *args, **kwargs, content_type="application/json")


class PlayerTestCase(BaseTestCase):
    def test_player_creation(self):
        response = self.post(
            "/players/", data=[{"name": "test_player1"}, {"name": "test_player2"}]
        )
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["players"][0]["name"], "test_player1")
        self.assertEqual(data["players"][1]["name"], "test_player2")
        self.assertEqual(data["players"][0]["cpu"], False)
        self.assertEqual(data["players"][1]["cpu"], False)

    def test_player_creation_with_cpu(self):
        response = self.post(
            "/players/",
            data=[{"name": "test_player1"}, {"name": "test_player2", "cpu": True}],
        )
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["players"][1]["cpu"], True)

    def test_player_creation_with_no_name(self):
        response = self.post(
            "/players/", data=[{"name": "test_player1"}, {"cpu": True}]
        )
        self.assertEqual(response.status_code, 400)

    def test_player_name_is_unique(self):
        self.post(
            "/players/", data=[{"name": "test_player1"}, {"name": "test_player2"}]
        )
        response = self.post(
            "/players/", data=[{"name": "test_player1"}, {"name": "test_player2"}]
        )
        self.assertEqual(response.status_code, 400)


class MatchTestCase(BaseTestCase):
    def setUp(self):
        self.player1 = "test_player1"
        self.player2 = "test_player2"
        for player in [self.player1, self.player2]:
            Player.objects.create(name=player)
        self.player3 = "cpu"
        Player.objects.create(name=self.player3, cpu=True)
        super().setUp()

    def test_tie_match(self):
        match = {
            "player1": self.player1,
            "player2": self.player2,
            "player1_choice": "ROCK",
            "player2_choice": "ROCK",
        }
        response = self.post("/matches/", data=match)

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["winner"], None)

    def test_rock_wins(self):
        match = {
            "player1": self.player1,
            "player2": self.player2,
            "player1_choice": "ROCK",
            "player2_choice": "SCISSORS",
        }
        response = self.post("/matches/", data=match)

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["winner"]["name"], self.player1)

    def test_paper_wins(self):
        match = {
            "player1": self.player1,
            "player2": self.player2,
            "player1_choice": "PAPER",
            "player2_choice": "ROCK",
        }
        response = self.post("/matches/", data=match)

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["winner"]["name"], self.player1)

    def test_scissors_wins(self):
        match = {
            "player1": self.player1,
            "player2": self.player2,
            "player1_choice": "SCISSORS",
            "player2_choice": "PAPER",
        }
        response = self.post("/matches/", data=match)

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["winner"]["name"], self.player1)

    def test_invalid_choice(self):
        match = {
            "player1": self.player1,
            "player2": self.player2,
            "player1_choice": "ROCK",
            "player2_choice": "INVALID",
        }
        response = self.post("/matches/", data=match)

        self.assertEqual(response.status_code, 400)

    def test_invalid_player(self):
        match = {
            "player1": "INVALID",
            "player2": self.player2,
            "player1_choice": "ROCK",
            "player2_choice": "PAPER",
        }
        response = self.post("/matches/", data=match)

        self.assertEqual(response.status_code, 400)

    def test_match_against_cpu(self):
        match = {
            "player1": self.player1,
            "player2": self.player3,
            "player1_choice": "ROCK",
        }
        response = self.post("/matches/", data=match)

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(data["player2_choice"], None)


class ScoreTestCase(BaseTestCase):
    def setUp(self):
        self.player1 = "test_player1"
        self.player2 = "test_player2"
        self.players = []
        for player in [self.player1, self.player2]:
            self.players.append(Player.objects.create(name=player))
        super().setUp()

    def test_initial_score(self):
        response = self.get(
            "/scores/", {"player1": self.player1, "player2": self.player2}
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[self.player1], 0)
        self.assertEqual(data[self.player2], 0)

    def test_score_after_match(self):
        won_matches = 3
        for _ in range(won_matches):
            Match.objects.create(
                player1=self.players[0],
                player2=self.players[1],
                player1_choice="ROCK",
                player2_choice="SCISSORS",
            )

        response = self.get(
            "/scores/", {"player1": self.player1, "player2": self.player2}
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[self.player1], won_matches)
        self.assertEqual(data[self.player2], 0)
