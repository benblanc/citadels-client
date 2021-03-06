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


@app.route("/select_character/<string:game_uuid>/<string:player_uuid>/<int:amount_players>/<string:player_crown>/<int:amount_removed_characters>", methods=['POST'])
def select_character(game_uuid, player_uuid, amount_players, player_crown, amount_removed_characters):
    return select_character_run(game_uuid, player_uuid, amount_players, string_to_bool(player_crown), amount_removed_characters)


@app.route("/receive_income/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def receive_income(game_uuid, player_uuid):
    return receive_income_run(game_uuid, player_uuid)


@app.route("/keep_card/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def keep_card(game_uuid, player_uuid):
    return keep_card_run(game_uuid, player_uuid)


@app.route("/build_district/<string:game_uuid>/<string:player_uuid>/<string:player_buildings>", methods=['POST'])
def build_district(game_uuid, player_uuid, player_buildings):
    return build_district_run(game_uuid, player_uuid, string_to_list(player_buildings))


@app.route("/use_main_character_ability/<string:game_uuid>/<string:player_uuid>/<string:current_character>", methods=['POST'])
def use_main_character_ability(game_uuid, player_uuid, current_character):
    return use_main_character_ability_run(game_uuid, player_uuid, current_character)


@app.route("/use_secondary_character_ability/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def use_secondary_character_ability(game_uuid, player_uuid):
    return use_secondary_character_ability_run(game_uuid, player_uuid)


@app.route("/use_district_ability/<string:game_uuid>/<string:player_uuid>/<string:district>/<string:player_buildings>", methods=['POST'])
def use_district_ability(game_uuid, player_uuid, district, player_buildings):
    return use_district_ability_run(game_uuid, player_uuid, district, string_to_list(player_buildings))


@app.route("/end_turn/<string:game_uuid>/<string:player_uuid>", methods=['POST'])
def end_turn(game_uuid, player_uuid):
    return end_turn_run(game_uuid, player_uuid)


@app.route("/game/<string:game_uuid>/<string:player_uuid>")
def game_player(game_uuid, player_uuid):
    return game_player_run(game_uuid, player_uuid)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8081)

    except Exception:
        logging.error(traceback.format_exc())

# TODO: add page to display all characters in game with info and put link in game page
# TODO: add page to display all districts in game with info and put link in game page
