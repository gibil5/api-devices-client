import setuptools

__version__ = open(".version").read()

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
