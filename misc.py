import json
from random import randint


def get_nonzero_random_value(max_abs_value: int) -> int:
    return randint(1, max_abs_value) if randint(0, 1) else randint(-max_abs_value, -1)


def read_json_from_file(fn):
    with open(fn, 'r') as json_in:
        settings = json.load(json_in)
    return settings


def write_json_to_file(fn, json_obj):
    with open(fn, 'w') as json_out:
        json.dump(json_obj, json_out, indent=4)
