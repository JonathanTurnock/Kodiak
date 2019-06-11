# FX Quants Analytics Engine Runner

The Analytics engine runner is a Flask application which is designed to run on a docker host orchestrating pipelines.
It has a single API endpoint ```/api/request``` which takes a POST. The JSON body must contain a url which is a git repo.
This git repo will be checked out, executed and the container will be removed once done.

TBC is a callback to report the status of the pipeline as it occurs.

## Getting Started
The first thing that is needed is a Git repository with an fxq-pipeline.yml file present.
See the following example [hello world](https://bitbucket.org/fxquants/aep-hello-world)

## Installing
I Highly recommend using PIPX to install the FXQuants Runner if installed locally to ensure you do not run into issues 
with other environments and CLI apps installed using PIP 
https://packaging.python.org/guides/installing-stand-alone-command-line-tools/

```
pipx install fxq-ae-runner
```

However I highly recommend using the official docker image for this and running the container with the Docker socket
passed into it. 
```
docker run -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock --name ae-runner fxquants/ae-runner:latest
``` 

## Usage
Simply post a request to the endpoint with the URL in the post body, you will see the request be carried out by the runner.
```
Request:
curl -d '{"url":"https://bitbucket.org/fxquants/aep-hello-world.git"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/request

Response:
{"commit_changes":false,"name":"fxquants-aep-hello-world","run_id":"d011cb4f-40e5-4ce3-9ccd-bd23cca3ba23","status":"IN_PROGRESS","steps":[{"commit_changes":false,"image":"alpine","name":"Hello World With Bash","script":[{"instruction":"echo Hello World","output":[]}],"status":"PENDING"}]}
```

Make sure to use Https for open repos so that you dont need to add authentication.

Alternatively with private repos you can provide an ssh based url but this will take additional setup.
Exec into the container using SSH, Generate an SSH Key and Exchange Keys with your Git service provider.

```
curl -d '{"url":"git@bitbucket.org:fxquants/aep-hello-world.git"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/request
```

## Contributing

Contributions are most welcome to the project, please raise issues first and contribute in response to the issue with a pull request.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://bitbucket.org/fxquants/fxq-ioc-core/downloads/?tab=tags). 

## Authors

* **Jonathan Turnock** - *Initial work* - [fxquants - profile](https://fxquants.atlassian.net/people/5c4e3005043b4f5d172a732a)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details