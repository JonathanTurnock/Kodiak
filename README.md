# FX Quants Analytics Engine Runner

The Analytics engine runner is a python flask application, it exposes an API and connects to the local docker environment
to allow scheduling of and execution of an fxq-pipeline.

## Getting Started
The first thing that is needed is a Git repository with an fxq-pipeline.yml file present.
See the following example [hello world](https://bitbucket.org/fxquants/aep-hello-world)

## Installing
I Highly recommend using PIPX to install the FXQuants Runner to ensure you do not run into issues with other environments and CLI apps installed using PIP 
https://packaging.python.org/guides/installing-stand-alone-command-line-tools/

```
pipx install fxq-ae-runner
```

## Usage
Simply start the application via the command line

```
fxq-ae-runner
```

## Contributing

Contributions are most welcome to the project, please raise issues first and contribute in response to the issue with a pull request.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://bitbucket.org/fxquants/fxq-ioc-core/downloads/?tab=tags). 

## Authors

* **Jonathan Turnock** - *Initial work* - [fxquants - profile](https://fxquants.atlassian.net/people/5c4e3005043b4f5d172a732a)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details