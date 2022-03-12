import logging, traceback, os, requests

from flask import Flask

from controllers.controller import *

from utils.helpers import *

app = Flask(__name__)

config_path = "./config/%s.json" % os.environ['PYTHON_ENV']  # set path to config

if not os.path.isfile(config_path):  # check if file does not exist
    print("PYTHON_ENV is invalid. Review the value and try again.")
    exit(1)  # exit script with "issue" code

create_environment_variables(config_path)  # load settings from config file


@app.route("/")
def index():
    return index_run()


@app.route("/join_game", methods=['POST'])
def join_game():
    return join_game_run()


@app.route("/create_game", methods=['POST'])
def create_game():
    return create_game_run()


@app.route("/start_game/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def start_game(game_uuid, player_uuid):
    return start_game_run(game_uuid, player_uuid)


@app.route("/select_character/<string:game_uuid>/<string:player_uuid>/<int:amount_players>/<string:player_king>/<int:amount_removed_characters>", methods=['POST'])
def select_character(game_uuid, player_uuid, amount_players, player_king, amount_removed_characters):
    return select_character_run(game_uuid, player_uuid, amount_players, string_to_bool(player_king), amount_removed_characters)


@app.route("/receive_income/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def receive_income(game_uuid, player_uuid):
    return receive_income_run(game_uuid, player_uuid)


@app.route("/keep_card/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def keep_card(game_uuid, player_uuid):
    return keep_card_run(game_uuid, player_uuid)


@app.route("/game/<string:game_uuid>/<string:player_uuid>")
def game_player(game_uuid, player_uuid):
    return game_player_run(game_uuid, player_uuid)


if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=8081)

    except Exception:
        logging.error(traceback.format_exc())
