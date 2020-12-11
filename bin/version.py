import os
from datetime import datetime
from distutils import util

VERSION = ".version"


def configure_version():
    ci = bool(util.strtobool(os.getenv("CI", "False")))
    circle_tag = os.getenv("CIRCLE_TAG")

    if ci and circle_tag:
        version = circle_tag
    elif ci:
        # Its assumed that when running in CI the branch is master
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d.%H%M")
        version = f"master.{timestamp}"
    else:
        version = "0.0.0"

    with open(VERSION, "w+") as f:
        f.write(version)


if __name__ == '__main__':
    configure_version()
