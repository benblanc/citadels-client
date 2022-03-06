import re


def validate_uuid(uuid):
    return re.match("^([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})$", uuid)


def validate_player_name(name):
    return re.match("^[a-zA-Z0-9_]+$", name)


def validate_description(description):
    return re.match("[a-zA-Z0-9_]+", description)


def validate_card_name(name):
    return re.match("^[a-zA-Z]+$", name)
