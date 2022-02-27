from flask import render_template, request, redirect

from controllers.endpoints import *
from controllers.validators import *

from utils.helpers import *


def index_run():
    games = []

    response_games = get_games()

    if is_request_successful(response_games.status_code):
        games = response_games.json()

    return render_template('index.html', games=games)


def join_game_run():
    game_uuid = request.values.get('game-to-join')
    player_name = request.values.get('player-name')

    print("game_uuid: ", game_uuid)
    print("player_name: ", player_name)

    if not game_uuid or not player_name:  # check if not none
        return redirect("/")

    if not validate_uuid(game_uuid) or not validate_name(player_name):  # check if invalid input
        return redirect("/")

    if request.method == 'POST':
        response_join_game = join_game(game_uuid, player_name)

        if not is_request_successful(response_join_game.status_code):
            return redirect("/")

        player_uuid = response_join_game.json()["uuid"]

        print("player_uuid: ", player_uuid)

        return redirect("/game/" + game_uuid + "/" + player_uuid)

    return redirect("/")


def create_game_run():
    player_name = request.values.get('player-name')
    game_description = request.values.get('game-description')

    game_name = "name_will_be_removed"

    print("player_name: ", player_name)
    print("game_description: ", game_description)

    if not player_name or not game_description:  # check if not none
        return redirect("/")

    if not validate_name(player_name) or not validate_description(game_description):  # check if invalid input
        return redirect("/")

    if request.method == 'POST':
        response_create_game = create_game(game_name, game_description)

        if not is_request_successful(response_create_game.status_code):
            return redirect("/")

        game_uuid = response_create_game.json()["uuid"]

        response_join_game = join_game(game_uuid, player_name)

        if not is_request_successful(response_join_game.status_code):
            return redirect("/")

        player_uuid = response_join_game.json()["uuid"]

        print("player_uuid: ", player_uuid)

        return redirect("/game/" + game_uuid + "/" + player_uuid)

    return redirect("/")


def start_game_run(game_uuid, player_uuid):
    if not validate_uuid(game_uuid) or not validate_uuid(player_uuid):
        return redirect("/")

    if request.method == 'POST':
        response_start_game = start_game(game_uuid, player_uuid)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def game_player_run(game_uuid, player_uuid):
    game = None
    players = None
    host = False

    response_game = get_game(game_uuid)

    if is_request_successful(response_game.status_code):
        game = response_game.json()

        pprint(game)

        response_get_characters = get_characters()

        if is_request_successful(response_get_characters.status_code):
            characters_full_info = response_get_characters.json()

        response_game_removed_characters = get_removed_characters(game_uuid)

        if is_request_successful(response_game_removed_characters.status_code):
            removed_characters = response_game_removed_characters.json()

            pprint(removed_characters)

            game["removed_characters"] = removed_characters

            open_removed_characters = list(filter(lambda character: character["open"] == True, removed_characters))
            closed_removed_characters = list(filter(lambda character: character["open"] == False, removed_characters))

            if characters_full_info:  # check if we have the full info on each character in the game
                for character in open_removed_characters:
                    character["order"] = list(filter(lambda _character: _character["name"] == character["name"], characters_full_info))[0]["order"]

                open_removed_characters = sorted(open_removed_characters, key=lambda character: character["order"], reverse=False)

            game["removed_character_pics"] = ["_back.jpg"] * len(closed_removed_characters)

            game["removed_character_pics"] += list(map(lambda x: x["name"].lower() + ".jpg", open_removed_characters))

        response_players = get_players(game["uuid"])

        if is_request_successful(response_players.status_code):
            players = response_players.json()

            pprint(players)

            player_seat = list(filter(lambda player: player["uuid"] == player_uuid, players))[0]["seat"]

            players = players[player_seat:] + players[:player_seat]  # update order of player in array so you are first, meaning you will be on top of the game UI

            for player in players:
                response_player_characters = get_player_characters(game_uuid, player["uuid"])

                if is_request_successful(response_player_characters.status_code):
                    characters = response_player_characters.json()

                    pprint(characters)

                    player["characters"] = characters

                    player["character_pics"] = []

                    for character in characters:
                        file_name = "_back.jpg"

                        if player["uuid"] == player_uuid or character["open"]:
                            file_name = character["name"].lower() + ".jpg"

                        player["character_pics"].append(file_name)

                    if player["uuid"] == player_uuid and player["hosting"]:
                        host = True

                response_player_cards = get_player_cards(game_uuid, player["uuid"])

                if is_request_successful(response_player_cards.status_code):
                    cards = response_player_cards.json()

                    pprint(cards)

                    player["cards"] = cards

                    player["card_pics"] = ["_back.jpg"] * len(cards)

                    if player["uuid"] == player_uuid:
                        player["card_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", cards))

                response_player_buildings = get_player_buildings(game_uuid, player["uuid"])

                if is_request_successful(response_player_buildings.status_code):
                    buildings = response_player_buildings.json()

                    pprint(buildings)

                    player["buildings"] = buildings

                    player["building_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", buildings))

    return render_template("game.html", game=game, players=players, player_uuid=player_uuid, host=host)