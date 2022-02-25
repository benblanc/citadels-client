import logging, traceback, os, requests

from flask import Flask, render_template, request, jsonify

from controllers import endpoints

from pprint import pprint

app = Flask(__name__)


# home route
@app.route("/")
def hello():
    return render_template('index.html', name='Jane', gender='Female')


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

        response_players = endpoints.get_players(base_url, game["uuid"])

        if response_players.status_code == 200:
            players = response_players.json()

            pprint(players)

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


if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=8081)

    except Exception:
        logging.error(traceback.format_exc())
