import os
from ruamel.yaml import YAML


def load_constants():
    config_path = os.path.join(os.path.dirname(__file__), "const.yaml")
    return YAML(typ="safe").load(open(config_path))