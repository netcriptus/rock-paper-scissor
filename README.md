# Rock, Paper, Scissors - The Game

This is an implementation of a basic back end for the rock, paper, scissors game.

### Dependencies

The easiest way to run this project is to have [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed.

Alternatively, it's also possible to run it locally, by having a python environment configured and running `pip install -r requirements.txt`

### Running the server

With docker:

```
make up
```

With a local installation:

```
uwsgi --ini uwsgi.ini
```

Both methods will run the API at `http://0.0.0.0:5000`

### Running the tests

```
make test
```


### API

The API documentation, with examples can be found on `http://0.0.0.0:5000`.

- `[POST, GET] /players/` - Bulk create and list players
- POST Parameters:
  - `name`: str
  - `cpu`: bool [optional | default: false]
  - Example: `curl -X POST /players/ -H "Content-Type: application/json" -d '[{"name": "example1"}, {"name": "computer", "cpu": true}]'`

This endpoint allows for multiple players to be created at once.

- `[POST, GET] /matches/` - Play and list matches between two players
- POST Parameters:
  - `player1`: str
  - `player2`: str
  - `player1_choice`: str [ROCK|PAPER|SCISSORS]
  - `player2_choice`: str [optional | default: random[ROCK|PAPER|SCISSORS]]
  - Example: `curl -X POST /matches/ -H "Content-Type: application/json" -d '{"player1": "example1", "player2": "example2", "player1_choice": "ROCK", "player2_choice": "PAPER"}'`

If Player2 is created as CPU, there's no need to send `player2_choice`, and the backend will randonly pick an option for it. The response will include the winner.

- `[GET] /scores/` - Get the score of 2 players
  - Example: `curl /scores/?player1=example1&player2=example2`

This query will return a dictionary with the player names as keys and their respective scores as values.


### Bug description

The game seems to work, but when we try to check score, it's always zero.
