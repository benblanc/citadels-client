import json, os


def read_json(file_path):
    with open(file_path) as file:
        return json.load(file)


def create_environment_variables(file_path):
    settings = read_json(file_path)

    for key, value in settings.items():
        os.environ[key.upper()] = value


def string_to_bool(text):
    status = False

    if text.lower() == "true":
        status = True

    return status


def string_to_list(text):
    return list(text.strip("]['").split(', '))


def get_citadels_api_base_url():
    return os.environ["CITADELS_API_BASE_URL"]


def get_logging_requests():
    return string_to_bool(os.environ["LOGGING_REQUESTS"])


def is_request_successful(status_code):
    response = False

    if 200 <= status_code < 300:
        response = True

    return response


def filter_on(key, required_value, elements, keep_first_item=True, equal_to=True):
    response = None

    if equal_to:  # check if values need to be equal
        items = list(filter(lambda element: element[key] == required_value, elements))  # keep elements where property value with key matches required value

    else:  # values should not be equal
        items = list(filter(lambda element: element[key] != required_value, elements))  # keep elements where property value with key matches required value

    if items:  # check if any elements
        response = items

        if keep_first_item:  # check if only first item is required
            response = items[0]  # get element

    return response
