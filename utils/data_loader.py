import os

import yaml


def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "../config/testdata.yaml")
    with open(file_path) as f:
        return yaml.safe_load(f)


data = load_data()


def get_user(role):
    return data["users"][role]
