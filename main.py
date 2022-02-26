import logging, traceback, os, requests

from flask import Flask, render_template, request, jsonify

from controllers import endpoints

from pprint import pprint

app = Flask(__name__)


# home route
@app.route("/")
def index():
    base_url = "http://127.0.0.1:8080"

    games = []

    response_games = endpoints.get_games(base_url)

    if response_games.status_code == 200:
        games = response_games.json()

    pprint(games)

    return render_template('index.html', games=games)


@app.route("/join_game", methods=['POST'])
def join_game():
    # game_uuid = request.form["game-to-join"]
    game_uuid = request.values.get('game-to-join')
    player_name = request.values.get('player-name')

    print("game_uuid: ", game_uuid)
    print("player_name: ", player_name)

    base_url = "http://127.0.0.1:8080"

    if request.method == 'POST':
        response_join_game = endpoints.join_game(base_url, game_uuid, player_name)

        if response_join_game.status_code == 201:
            player_uuid = response_join_game.json()
            print("player_uuid: ", player_uuid)

    response_game = endpoints.get_game(base_url, game_uuid)

    if response_game.status_code == 200:
        game = response_game.json()

        pprint(game)

    response_players = endpoints.get_players(base_url, game_uuid)

    if response_players.status_code == 200:
        players = response_players.json()

        pprint(players)

    return render_template("lobby.html")


# serving form web page
@app.route("/my-form")
def form():
    return render_template('form.html')


# handling form data
@app.route('/form-handler', methods=['POST'])
def handle_data():
    return jsonify(request.form)


@app.route("/characters")
def characters():
    pics = ["_back.jpg"]

    query = {
        "sort_order": "asc",
        "order_by": "order"
    }

    response = requests.get('http://localhost:8080/cards/characters', params=query)

    if response.status_code == 200:
        characters = response.json()

        print(characters)

        pics = list(map(lambda x: x["name"].lower() + ".jpg", characters))

        print(pics)

    return render_template("characters.html", pics=pics)


@app.route("/game/<string:game_uuid>")
def game(game_uuid):
    pics_characters = ["_back.jpg"]
    pics_districts = ["_back.jpg"]

    base_url = "http://127.0.0.1:8080"

    response_game = endpoints.get_game(base_url, game_uuid)

    if response_game.status_code == 200:
        game = response_game.json()

        pprint(game)

        response_game_removed_characters = endpoints.get_removed_characters(base_url, game_uuid)

        if response_game_removed_characters.status_code == 200:
            removed_characters = response_game_removed_characters.json()

            pprint(removed_characters)

            game["removed_characters"] = removed_characters

            game["removed_character_pics"] = ["_back.jpg"] * len(removed_characters)

            game["removed_character_pics"] = list(map(lambda x: x["name"].lower() + ".jpg", removed_characters))

        response_players = endpoints.get_players(base_url, game["uuid"])

        if response_players.status_code == 200:
            players = response_players.json()

            pprint(players)

            for player in players:
                response_player_characters = endpoints.get_player_characters(base_url, game_uuid, player["uuid"])

                if response_player_characters.status_code == 200:
                    characters = response_player_characters.json()

                    pprint(characters)

                    player["characters"] = characters

                    player["character_pics"] = list(map(lambda x: x["name"].lower() + ".jpg", characters))

                response_player_cards = endpoints.get_player_cards(base_url, game_uuid, player["uuid"])

                if response_player_cards.status_code == 200:
                    cards = response_player_cards.json()

                    pprint(cards)

                    player["cards"] = cards

                    player["card_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", cards))

                response_player_buildings = endpoints.get_player_buildings(base_url, game_uuid, player["uuid"])

                if response_player_buildings.status_code == 200:
                    buildings = response_player_buildings.json()

                    pprint(buildings)

                    player["buildings"] = buildings

                    player["building_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", buildings))

    query = {
        "sort_order": "asc",
        "order_by": "order"
    }

    response = requests.get('http://localhost:8080/cards/characters', params=query)

    if response.status_code == 200:
        characters = response.json()

        pprint(characters)

        pics_characters = list(map(lambda x: x["name"].lower() + ".jpg", characters))

        print(pics_characters)

    return render_template("game.html", players=players, pics=pics_characters)


@app.route("/game/<string:game_uuid>/<string:player_uuid>")
def game_player(game_uuid, player_uuid):
    pics_characters = ["_back.jpg"]
    pics_districts = ["_back.jpg"]

    base_url = "http://127.0.0.1:8080"

    response_game = endpoints.get_game(base_url, game_uuid)

    if response_game.status_code == 200:
        game = response_game.json()

        pprint(game)

        response_get_characters = endpoints.get_characters(base_url)

        if response_get_characters.status_code == 200:
            characters_full_info = response_get_characters.json()

        response_game_removed_characters = endpoints.get_removed_characters(base_url, game_uuid)

        if response_game_removed_characters.status_code == 200:
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

        response_players = endpoints.get_players(base_url, game["uuid"])

        if response_players.status_code == 200:
            players = response_players.json()

            pprint(players)

            player_seat = list(filter(lambda player: player["uuid"] == player_uuid, players))[0]["seat"]

            players = players[player_seat:] + players[:player_seat]  # update order of player in array so you are first, meaning you will be on top of the game UI

            for player in players:
                response_player_characters = endpoints.get_player_characters(base_url, game_uuid, player["uuid"])

                if response_player_characters.status_code == 200:
                    characters = response_player_characters.json()

                    pprint(characters)

                    player["characters"] = characters

                    player["character_pics"] = []

                    for character in characters:
                        file_name = "_back.jpg"

                        if player["uuid"] == player_uuid or character["open"]:
                            file_name = character["name"].lower() + ".jpg"

                        player["character_pics"].append(file_name)

                response_player_cards = endpoints.get_player_cards(base_url, game_uuid, player["uuid"])

                if response_player_cards.status_code == 200:
                    cards = response_player_cards.json()

                    pprint(cards)

                    player["cards"] = cards

                    player["card_pics"] = ["_back.jpg"] * len(cards)

                    if player["uuid"] == player_uuid:
                        player["card_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", cards))

                response_player_buildings = endpoints.get_player_buildings(base_url, game_uuid, player["uuid"])

                if response_player_buildings.status_code == 200:
                    buildings = response_player_buildings.json()

                    pprint(buildings)

                    player["buildings"] = buildings

                    player["building_pics"] = list(map(lambda x: x["name"].replace(" ", "_").lower() + ".jpg", buildings))

    return render_template("game.html", game=game, players=players, player_uuid=player_uuid)


if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=8081)

    except Exception:
        logging.error(traceback.format_exc())
