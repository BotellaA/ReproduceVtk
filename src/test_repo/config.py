import os
from sys import platform


def default_config():
    os.environ["DEFAULT_HOST"] = "localhost"
    os.environ["DEFAULT_PORT"] = "1234"


def test_config(path):
    default_config()
    print(f"{os.path.dirname(__file__)=}", flush=True)
    os.environ["DATA_FOLDER_PATH"] = os.path.join(path, 
     "data"
    )
    print(f"{os.environ.get('DATA_FOLDER_PATH')=}", flush=True)
