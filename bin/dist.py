import configparser
import os
from os.path import expanduser

PYPIRC = ".pypirc"


def configure_pypirc():
    fury_token = os.getenv("FURY_AUTH")

    config = configparser.ConfigParser()
    config["distutils"] = {"index-servers": "fury"}
    config["fury"] = {
        "repository": "https://pypi.fury.io/electric/",
        "username": fury_token,
        "password": "",
    }

    home = expanduser("~")
    path = f"{home}/{PYPIRC}"
    with open(path, "w+") as configfile:
        config.write(configfile)


if __name__ == '__main__':
    configure_pypirc()
