import pathlib

from setuptools import setup

setup(
    name='kodiak-ae-agent',
    version='0.0.17-SNAPSHOT',
    packages=[
        'kodiak.agent',
        'kodiak.agent.callback',
        'kodiak.agent.factory',
        'kodiak.agent.model',
        'kodiak.agent.service',
        'kodiak.server'
    ],
    url='https://bitbucket.org/fxqlabs-oss/kodiak/',
    license='MIT',
    author='Jonathan Turnock',
    author_email='jonathan.turnock@outlook.com',
    description='Docker host orchestration app to run pipelines',
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=[
        'click',
        'docker',
        'flask',
        'gitpython',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['kodiak=kodiak.cli:main'],
    }
)
