import requests, json

from utils.helpers import *

from pprint import pprint


def log_response(response):
    if get_logging_requests():
        print("request url: ", response.request.url)
        print("request body:")

        content = ""
        if response.request.body:  # check if there is content
            content = json.loads(response.request.body.decode('utf8'))

        pprint(content)
        print("-" * 50)
        print("response status code: ", response.status_code)
        print("response body:")

        content = response.text
        if response.text:  # check if there is content
            content = response.json()

        pprint(content)
        print("=" * 100)


def get_games():
    response = requests.get(url=get_citadels_api_base_url() + "/game")

    log_response(response)

    return response


def get_game(game_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid)

    log_response(response)

    return response


def create_game(description):
    payload = {
        "description": description
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/action.create", json=payload)

    log_response(response)

    return response


def join_game(game_uuid, name):
    payload = {
        "name": name
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/action.join", json=payload)

    log_response(response)

    return response


def start_game(game_uuid, player_uuid):
    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.start")

    log_response(response)

    return response


def get_players(game_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players")

    log_response(response)

    return response


def get_player(game_uuid, player_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid)

    log_response(response)

    return response


def get_player_characters(game_uuid, player_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/characters")

    log_response(response)

    return response


def get_player_cards(game_uuid, player_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/cards")

    log_response(response)

    return response


def get_player_buildings(game_uuid, player_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/buildings")

    log_response(response)

    return response


def get_possible_characters(game_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/possible_characters")

    log_response(response)

    return response


def get_removed_characters(game_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/removed_characters")

    log_response(response)

    return response


def get_characters():
    query_params = {
        "sort_order": "asc",
        "order_by": "order"
    }

    response = requests.get(url=get_citadels_api_base_url() + "/cards/characters", params=query_params)

    log_response(response)

    return response


def select_character(game_uuid, player_uuid, name, remove):
    payload = {
        "name": name,
        "remove": remove
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.select", json=payload)

    log_response(response)

    return response


def receive_gold(game_uuid, player_uuid):
    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.receive_gold")

    log_response(response)

    return response


def draw_cards(game_uuid, player_uuid):
    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.draw_cards")

    log_response(response)

    return response


def get_drawn_cards(game_uuid, player_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/drawn_cards")

    log_response(response)

    return response


def keep_card(game_uuid, player_uuid, names):
    payload = {
        "names": names
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.keep_card", json=payload)

    log_response(response)

    return response


def build_district(game_uuid, player_uuid, name):
    payload = {
        "name": name
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.build", json=payload)

    log_response(response)

    return response


def use_ability(game_uuid, player_uuid, main=False, character_name="", district_names=None, other_player_uuid=""):
    payload = {
        "main": main,
        "name": {
            "character": character_name,
            "districts": district_names or []
        },
        "player_uuid": other_player_uuid
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.use_ability", json=payload)

    log_response(response)

    return response


def use_building_ability(game_uuid, player_uuid, name, target_name=""):
    payload = {
        "name": target_name
    }

    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/buildings/" + name + "/action.use_ability", json=payload)

    log_response(response)

    return response


def end_turn(game_uuid, player_uuid):
    response = requests.post(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/players/" + player_uuid + "/action.end_turn")

    log_response(response)

    return response


def get_deck_characters(game_uuid):
    response = requests.get(url=get_citadels_api_base_url() + "/game/" + game_uuid + "/deck_characters")

    log_response(response)

    return response
