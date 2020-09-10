import setuptools

__version__ = "1.6.4"

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
    url='https://github.com/ElectricAI/api-devices',
    packages=setuptools.find_packages(exclude="tests"),
    install_requires=requirements,
    classifiers=[],
)
