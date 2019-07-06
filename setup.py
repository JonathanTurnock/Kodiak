import pathlib

from setuptools import setup

setup(
    name='fxq-ae-runner',
    version='0.0.12',
    packages=[
        'fxq.ae.runner',
        'fxq.ae.runner.callback',
        'fxq.ae.runner.factory',
        'fxq.ae.runner.model',
        'fxq.ae.runner.service',
    ],
    url='https://bitbucket.org/fxquants/ae-runner/',
    license='MIT',
    author='Jonathan Turnock',
    author_email='jonathan.turnock@fxquants.net',
    description='Analytics Engine Runner Client, Provisions and executes docker pipelines from git repo yml',
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=[
        'docker',
        'flask',
        'fxq-core',
        'gitpython',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['fxq-ae-runner=fxq.ae.runner.cli:main'],
    }
)
