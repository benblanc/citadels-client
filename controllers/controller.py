from flask import render_template

from controllers import endpoints

from utils.helpers import *


def index_run():
    games = []

    response_games = endpoints.get_games()

    if is_request_successful(response_games.status_code):
        games = response_games.json()

    return render_template('index.html', games=games)
