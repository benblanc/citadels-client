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

    if not game_uuid or not player_name:  # check if not none
        return redirect("/")

    if not validate_uuid(game_uuid) or not validate_player_name(player_name):  # check if invalid input
        return redirect("/")

    if request.method == 'POST':
        response_join_game = join_game(game_uuid, player_name)

        if not is_request_successful(response_join_game.status_code):
            return redirect("/")

        return redirect("/game/" + game_uuid + "/" + response_join_game.json()["uuid"])

    return redirect("/")


def create_game_run():
    player_name = request.values.get('player-name')
    game_description = request.values.get('game-description')

    game_name = "name_will_be_removed"

    if not player_name or not game_description:  # check if not none
        return redirect("/")

    if not validate_player_name(player_name) or not validate_description(game_description):  # check if invalid input
        return redirect("/")

    if request.method == 'POST':
        response_create_game = create_game(game_name, game_description)

        if not is_request_successful(response_create_game.status_code):
            return redirect("/")

        game_uuid = response_create_game.json()["uuid"]

        response_join_game = join_game(game_uuid, player_name)

        if not is_request_successful(response_join_game.status_code):
            return redirect("/")

        return redirect("/game/" + game_uuid + "/" + response_join_game.json()["uuid"])

    return redirect("/")


def start_game_run(game_uuid, player_uuid):
    if not validate_uuid(game_uuid) or not validate_uuid(player_uuid):
        return redirect("/")

    if request.method == 'POST':
        start_game(game_uuid, player_uuid)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def select_character_run(game_uuid, player_uuid, amount_players, player_king, amount_removed_characters):
    character_name = request.values.get('character-name')
    character_remove = ""

    if amount_players == 2 and not player_king or amount_players == 2 and amount_removed_characters > 1:  # character only needs to be removed when game has two players and the first player to select (the king) does not discard one
        character_remove = request.values.get('character-remove')

        if not character_remove:  # check if not none
            return redirect("/game/" + game_uuid + "/" + player_uuid)

        if not validate_card_name(character_remove):  # check if invalid input
            return redirect("/game/" + game_uuid + "/" + player_uuid)

    if not character_name:  # check if not none
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if not validate_card_name(character_name):  # check if invalid input
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if character_name == character_remove:  # check if character to keep is same as character to remove
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if request.method == 'POST':
        select_character(game_uuid, player_uuid, character_name, character_remove)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def receive_income_run(game_uuid, player_uuid):
    income_type = request.values.get('income-type')

    if not income_type:  # check if not none
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if not validate_income_type(income_type):  # check if invalid input
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if request.method == 'POST':
        if income_type == "coins":
            receive_coins(game_uuid, player_uuid)

        elif income_type == "cards":
            draw_cards(game_uuid, player_uuid)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def keep_card_run(game_uuid, player_uuid):
    card_keep = request.values.get('card-keep')

    if not card_keep:  # check if not none
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if not validate_card_name(card_keep):  # check if invalid input
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if request.method == 'POST':
        keep_card(game_uuid, player_uuid, card_keep)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def build_district_run(game_uuid, player_uuid, player_buildings):
    district_name = request.values.get('district-name')

    if not district_name:  # check if not none
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if not validate_card_name(district_name):  # check if invalid input
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if district_name in player_buildings:
        return redirect("/game/" + game_uuid + "/" + player_uuid)

    if request.method == 'POST':
        build_district(game_uuid, player_uuid, district_name)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def use_main_character_ability_run(game_uuid, player_uuid, current_character):
    if current_character in ["assassin", "thief"]:
        character_name = request.values.get('character-name')

        if not character_name:  # check if not none
            return redirect("/game/" + game_uuid + "/" + player_uuid)

        if not validate_card_name(character_name):  # check if invalid input
            return redirect("/game/" + game_uuid + "/" + player_uuid)

    elif current_character == "magician":
        other_player_uuid = request.values.get('player-uuid')
        card_names = request.form.getlist('card-name')

        if not other_player_uuid:  # check if not none
            return redirect("/game/" + game_uuid + "/" + player_uuid)

        if card_names:  # check if some checkboxes are marked
            if not validate_card_names(card_names):  # check if invalid input
                return redirect("/game/" + game_uuid + "/" + player_uuid)

    elif current_character == "warlord":
        player_district = request.values.get('player-district')

        if not player_district:  # check if not none
            return redirect("/game/" + game_uuid + "/" + player_uuid)

        items = player_district.split("|")  # split on whitespace

        if len(items) != 2:  # check if expected amount of items
            return redirect("/game/" + game_uuid + "/" + player_uuid)

        other_player_uuid = items[0]  # get uuid of player to target
        district_name = items[1]  # get district to target

        if not validate_uuid(other_player_uuid):  # check if invalid input
            return redirect("/game/" + game_uuid + "/" + player_uuid)

        if not validate_card_name(district_name):  # check if invalid input
            return redirect("/game/" + game_uuid + "/" + player_uuid)

    if request.method == 'POST':
        if current_character in ["assassin", "thief"]:
            use_ability(game_uuid, player_uuid, main=True, character_name=character_name)

        elif current_character == "magician":
            if card_names:  # check if some checkboxes are marked
                use_ability(game_uuid, player_uuid, main=True, district_names=card_names)

            else:  # no marked checkboxes
                use_ability(game_uuid, player_uuid, main=True, other_player_uuid=other_player_uuid)

        elif current_character == "warlord":
            use_ability(game_uuid, player_uuid, main=True, district_names=[district_name], other_player_uuid=other_player_uuid)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def use_secondary_character_ability_run(game_uuid, player_uuid):
    if request.method == 'POST':
        use_ability(game_uuid, player_uuid)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def end_turn_run(game_uuid, player_uuid):
    if request.method == 'POST':
        end_turn(game_uuid, player_uuid)

    return redirect("/game/" + game_uuid + "/" + player_uuid)


def game_player_run(game_uuid, player_uuid):
    game = None
    players = None
    host = False
    player_uuid_select_expected = None
    player_drawn_card_names = []
    player_drawn_card_pics = []
    player_buildings = None
    building_limit = 1
    possible_characters_to_assassinate_or_rob = []
    highest_score = 0
    winners = []

    characters_secondary_ability = [  # should be done through ability look-up
        "king",
        "bishop",
        "merchant",
        "warlord"
    ]

    response_game = get_game(game_uuid)

    if is_request_successful(response_game.status_code):
        game = response_game.json()

        response_get_characters = get_characters()

        if is_request_successful(response_get_characters.status_code):
            characters_full_info = response_get_characters.json()

        response_get_deck_characters = get_deck_characters(game_uuid)

        if is_request_successful(response_get_deck_characters.status_code):
            game["deck_characters"] = response_get_deck_characters.json()

        response_game_possible_characters = get_possible_characters(game_uuid)

        if is_request_successful(response_game_possible_characters.status_code):
            possible_characters = response_game_possible_characters.json()

            if characters_full_info:  # check if we have the full info on each character in the game
                for character in possible_characters:
                    character["order"] = filter_on("name", character["name"], characters_full_info)["order"]

                possible_characters = sorted(possible_characters, key=lambda character: character["order"], reverse=False)

            game["possible_characters"] = possible_characters

        response_game_removed_characters = get_removed_characters(game_uuid)

        if is_request_successful(response_game_removed_characters.status_code):
            removed_characters = response_game_removed_characters.json()

            game["removed_characters"] = removed_characters

            open_removed_characters = filter_on("open", True, removed_characters, False) or []
            closed_removed_characters = filter_on("open", False, removed_characters, False) or []

            if characters_full_info:  # check if we have the full info on each character in the game
                for character in open_removed_characters:
                    character["order"] = filter_on("name", character["name"], characters_full_info)["order"]

                open_removed_characters = sorted(open_removed_characters, key=lambda character: character["order"], reverse=False)

            game["removed_character_pics"] = ["_back.jpg"] * len(closed_removed_characters)

            game["removed_character_pics"] += list(map(lambda x: x["name"].lower() + ".jpg", open_removed_characters))

        response_player_characters = get_player_characters(game_uuid, player_uuid)

        if is_request_successful(response_player_characters.status_code):
            character = filter_on("name", game["character_turn"], response_player_characters.json())

            if character:  # check if not none
                if game["character_turn"] == character["name"]:  # check if the turn character
                    response_drawn_cards = get_drawn_cards(game_uuid, player_uuid)

                    if is_request_successful(response_drawn_cards.status_code):
                        for card in response_drawn_cards.json():  # go through drawn cards
                            for index in range(card["amount"]):  # based on amount
                                player_drawn_card_names.append(card["name"])  # add name

                        player_drawn_card_pics = list(map(lambda name: name.replace(" ", "_").lower() + ".jpg", player_drawn_card_names))  # get pics for drawn cards

                    response_buildings = get_player_buildings(game_uuid, player_uuid)

                    if is_request_successful(response_buildings.status_code):
                        player_buildings = list(map(lambda building: building["name"], response_buildings.json()))  # get names of built districts in player's city

                    response_characters = get_characters()

                    if is_request_successful(response_characters.status_code):
                        building_limit = filter_on("name", character["name"], response_characters.json())["max_built"]  # get building limit for character

        if game["deck_characters"] and game["removed_characters"]:  # check if both properties have values
            possible_characters_to_assassinate_or_rob = filter_on("name", "assassin", game["deck_characters"], keep_first_item=False, equal_to=False)  # remove assassin from possible targets

            open_removed_characters = filter_on("open", True, game["removed_characters"], False) or []  # get all open remove characters

            for character in open_removed_characters:  # go over publically known removed characters
                possible_characters_to_assassinate_or_rob = filter_on("name", character["name"], possible_characters_to_assassinate_or_rob, keep_first_item=False, equal_to=False)  # remove character from possible targets

            if game["character_turn"] == "thief":  # check if it's the thief's turn
                possible_characters_to_assassinate_or_rob = filter_on("name", "thief", possible_characters_to_assassinate_or_rob, keep_first_item=False, equal_to=False)  # remove thief from possible targets

            if characters_full_info:  # check if we have the full info on each character in the game
                for character in possible_characters_to_assassinate_or_rob:
                    character["order"] = filter_on("name", character["name"], characters_full_info)["order"]

                possible_characters_to_assassinate_or_rob = sorted(possible_characters_to_assassinate_or_rob, key=lambda character: character["order"], reverse=False)

        response_players = get_players(game["uuid"])

        if is_request_successful(response_players.status_code):
            players = response_players.json()

            player_seat = filter_on("uuid", player_uuid, players)["seat"]

            players = players[player_seat:] + players[:player_seat]  # update order of player in array so you are first, meaning you will be on top of the game UI

            for player in players:
                if player["uuid"] == player_uuid and player["hosting"]:
                    host = True

                if player["select_expected"]:
                    player_uuid_select_expected = player["uuid"]

                response_player_characters = get_player_characters(game_uuid, player["uuid"])

                if is_request_successful(response_player_characters.status_code):
                    characters = response_player_characters.json()

                    player["characters"] = characters

                    player["current_character"] = filter_on("name", game["character_turn"], characters)

                    if characters_full_info:  # check if we have the full info on each character in the game
                        for character in characters:
                            character["order"] = filter_on("name", character["name"], characters_full_info)["order"]

                        characters = sorted(characters, key=lambda character: character["order"], reverse=False)

                    player["character_pics"] = []

                    for character in characters:
                        file_name = "_back.jpg"

                        if player["uuid"] == player_uuid or character["open"]:
                            file_name = character["name"].lower() + ".jpg"

                        player["character_pics"].append(file_name)

                        if character["assassinated"]:  # check if character is assassinated
                            possible_characters_to_assassinate_or_rob = filter_on("name", character["name"], possible_characters_to_assassinate_or_rob, keep_first_item=False, equal_to=False)  # remove character from possible targets

                response_player_cards = get_player_cards(game_uuid, player["uuid"])

                if is_request_successful(response_player_cards.status_code):
                    cards = response_player_cards.json()

                    player["cards"] = cards

                    player["card_names"] = []

                    player["card_pics"] = []

                    for card in cards:
                        file_name = "_back.jpg"

                        if player["uuid"] == player_uuid:
                            file_name = card["name"].replace(" ", "_").lower() + ".jpg"

                        for index in range(card["amount"]):
                            player["card_pics"].append(file_name)
                            player["card_names"].append(card["name"])

                    player["card_names_length"] = len(player["card_names"])

                response_player_buildings = get_player_buildings(game_uuid, player["uuid"])

                if is_request_successful(response_player_buildings.status_code):
                    buildings = response_player_buildings.json()

                    player["buildings"] = buildings

                    player["building_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", buildings))

                response_drawn_cards = get_drawn_cards(game_uuid, player["uuid"])

                if is_request_successful(response_drawn_cards.status_code):
                    player["drawn_cards"] = response_drawn_cards.json()

                if player["score"] == highest_score:  # check if player same high score
                    winners.append(player["name"])  # add player name to winners

                elif player["score"] > highest_score:  # check if player has higher score
                    highest_score = player["score"]  # set new high score
                    winners = [player["name"]]  # set player name as winner

    return render_template("game.html",
                           game=game, players=players, player_uuid=player_uuid, host=host,
                           player_uuid_select_expected=player_uuid_select_expected, amount_removed_characters=len(game["removed_characters"]),
                           player_drawn_card_pics=player_drawn_card_pics, player_buildings=str(player_buildings), building_limit=building_limit,
                           characters_secondary_ability=characters_secondary_ability, possible_characters_to_assassinate_or_rob=possible_characters_to_assassinate_or_rob,
                           highest_score=highest_score, winners=winners, player_drawn_card_names=player_drawn_card_names)
