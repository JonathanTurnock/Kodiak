import pathlib

import yaml
from setuptools import setup

with open('app.yml', 'r') as app_ymlf:
    config = yaml.load(app_ymlf, Loader=yaml.FullLoader)

setup(
    name=config["app"]["name"],
    version=config["app"]["version"],
    packages=config["app"]["setup"]["packages"],
    url=config["app"]["url"],
    license=config["app"]["license"],
    author=config["app"]["author"]["name"],
    author_email=config["app"]["author"]["email"],
    description=config["app"]["description"],
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=config["app"]["setup"]["install_requires"],
    entry_points={
        'console_scripts': ['kodiak=kodiak.cli:main'],
    }
)
