from flask import Blueprint, g
from sqlalchemy.exc import SQLAlchemyError

from ranker import app, logging
from ranker.api.utils import convert_request, make_response, content_is_valid, admin_required, auth_required
from ranker.db.game import Game
from ranker.db.utils import create_game
from ranker.schema.game import games_schema, game_schema
from ranker.schema.season import seasons_schema

config = app.config
game_bp = Blueprint("game", __name__, url_prefix="/games")


@game_bp.route("", methods=["GET"])
def get_games():
    games = Game.get_game()
    return games_schema.dumps(games)


@game_bp.route("/<int:_id>", methods=["GET"])
def get_game(_id):
    game = Game.get_game(_id)
    return game_schema.dumps(game)


@game_bp.route("/<int:_id>/seasons", methods=["GET"])
def get_game_seasons(_id):
    game = Game.get_game(_id)
    seasons = game.seasons
    return seasons_schema.dumps(seasons)


@game_bp.route("/new", methods=["POST"])
@auth_required
@admin_required
def new_game():
    if not g.user.admin:
        return make_response("You are not an authorized administrator", 403)

    try:
        content = convert_request()
    except AssertionError as err:
        logging.error('Error: Challenge request failed: ', err)
        return make_response("Sorry, that's not a valid request", 400)
    if not content_is_valid(content, 'title', 'img', 'description'):
        return make_response("Sorry, that's not a valid game request", 400)

    title = content["title"]
    img = content["img"]
    description = content["description"]
    # TODO: V3 -> Implement Game Based Rounds
    max_rounds = 5
    min_rounds = 3

    try:
        create_game(title, img, description, max_rounds, min_rounds)
    except SQLAlchemyError as err:
        logging.error("Error: Could not create game: ", err)
        return make_response("Sorry, that game could not be created. Check your fields and try again", 400)
    return make_response("You have created the game: {0}".format(title), 200)
