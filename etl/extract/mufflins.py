import json


def mufflins(filename="data/mufflins.json"):
    """ Extract data from the JSON for Mufflins University """
    with open(filename, "r") as fp:
        return json.load(fp)
