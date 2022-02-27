import json, os


def read_json(file_path):
    with open(file_path) as file:
        return json.load(file)


def create_environment_variables(file_path):
    settings = read_json(file_path)

    for key, value in settings.items():
        os.environ[key.upper()] = value


def get_citadels_api_base_url():
    return os.environ["CITADELS_API_BASE_URL"]


def get_logging_requests():
    return bool(os.environ["LOGGING_REQUESTS"])


def is_request_successful(status_code):
    response = False

    if 200 <= status_code < 300:
        response = True

    return response
