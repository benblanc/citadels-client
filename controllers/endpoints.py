import requests, json

from pprint import pprint

LOGGING_REQUESTS = False


def log_response(response):
    if LOGGING_REQUESTS:
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


def get_game(base_url, game_uuid):
    response = requests.get(url=base_url + "/game/" + game_uuid)

    log_response(response)

    return response


def get_players(base_url, game_uuid):
    response = requests.get(url=base_url + "/game/" + game_uuid + "/players")

    log_response(response)

    return response


def get_player(base_url, game_uuid, player_uuid):
    response = requests.get(url=base_url + "/game/" + game_uuid + "/players/" + player_uuid)

    log_response(response)

    return response


def get_player_characters(base_url, game_uuid, player_uuid):
    response = requests.get(url=base_url + "/game/" + game_uuid + "/players/" + player_uuid + "/characters")

    log_response(response)

    return response


def get_player_cards(base_url, game_uuid, player_uuid):
    response = requests.get(url=base_url + "/game/" + game_uuid + "/players/" + player_uuid + "/cards")

    log_response(response)

    return response


def get_player_buildings(base_url, game_uuid, player_uuid):
    response = requests.get(url=base_url + "/game/" + game_uuid + "/players/" + player_uuid + "/buildings")

    log_response(response)

    return response
