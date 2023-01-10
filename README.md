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


### Development, trade-offs and caveats

This project was supposed to be timeboxed to 3 hours, so I had to cut some corners.

**Chosen tools**

- Django; as base framework
- Django Rest Framework; for validation and enpoints
- Postgres; as database

I decided to use Django and Django Rest Framework, which could be considered an overkill for such a small project, but that allow for faster development since it takes care of a lot of common configuration. I used Postgresql instead of the native SQLite3 for better performance.


**Trade-offs**

The specs required the players to take separate turns to play, which could translate to 2 separate requests to the backend. My choice was to have the front end take one turn at a time but send both choices in one request. Unfortunatelly, there was no spare time to implement the front end.

The scores are not kept as a consolidated values. This is done in favor of using a simple database scheme, but will represent a bottleneck in a stress test.

There's no explicit command to save a game, but the whole history of matches between two players is always saved, and it can be picked up again at any point in time.

**Caveats**

Not all corner cases were taken care off. This code would never be approved by QA. For example, the uniqueness of a player name is only properly validated when it's created in different requests. Sending a list with two or more repeated names will crash the server. Only basic input validation was taken care of.

The configuration of the project is not production-ready. The debug options are still active and the server secret is hardcoded, as well as the database credentials.


**Future development**

If given more time, the next steps would be, in no particular order:
- Create a front end interface (possibly with Jinja2)
- Create more input validators
- Consolidate scores in the database
- Get configuration options from environment to allow for deploy in different places; remove hardcoded secrets/credentials.
