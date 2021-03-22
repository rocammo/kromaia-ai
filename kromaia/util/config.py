import json

from enum import Enum


class Environment(Enum):
    DEVELOPMENT = 1
    PRODUCTION = 2


def load_config(file: str):
    with open(file) as f:
        config = json.load(f)

    return config


def get_config(file: str, environment: str):
    config = load_config(file)

    environments = {
        "dev": Environment.DEVELOPMENT,
        "prod": Environment.PRODUCTION
    }

    if environments[environment] == Environment.DEVELOPMENT:
        return config["dev"]
    elif environments[environment] == Environment.PRODUCTION:
        return config["prod"]
