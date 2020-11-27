import os
from datetime import datetime
from distutils import util

import setuptools

CI = bool(util.strtobool(os.getenv("CI", "False")))
CIRCLE_BUILD_NUM = os.getenv("CIRCLE_BUILD_NUM")
CIRCLE_TAG = os.getenv("CIRCLE_TAG")

if CI and CIRCLE_TAG:
    version = CIRCLE_TAG
elif CI:
    # Its assumed that when running in CI the branch is master
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d.%H%M")
    version = f"master.{timestamp}"
else:
    version = "0.0.0"

__version__ = version

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='api-devices-client',
    version=__version__,
    author='IT Enablement',
    author_email='',
    description="API-devices python client package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ElectricAI/api-devices-client',
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    install_requires=requirements,
    classifiers=[],
)
