# FX Quants Analytics Engine Runner

The Analytics engine runner is a Flask application which is designed to run on a docker host.
Its purpose is to take a request from a Strategy Scheduler and run it using the following technique:   
1. Receive GIT URL    
2. Clone GIT repo   
3. Parse GIT repo YML   
4. Extract Image   
5. Create Image and keep it alive   
4. Execute commands in container and capture STDOUT   
5. Stream STDOUT to the Callback (back to the scheduler)   
6. Stop container when all commands are finished and all processes stopped.   
7. Delete the container.   
   
It has a single API endpoint ```/api/request``` which takes a POST. The JSON body must contain a url which is a git repo.
This git repo will be checked out, executed and the created container will be removed once done.

To enable the callback functionality to update a persistent store with the results of the pipeline define the following endpoints as environment variables.
All URL's must be Fully Qualified API endpoints built to digest the JSON.
```
PIPELINE_CALLBACK_URL - Takes a main pipeline json object 
STEP_CALLBACK_URL - Takes a step json object
CMD_CALLBACK_URL - Takes a cmd json object
```
You can take, the top level (pipelines) and only update on major changes.   
The mid level (pipeline & step) and only update on step changes.
The lowest level (pipeline, step & cmd) and update as each and every output is received.

All models above contain the models below. So you can always get all of the detail, just less frequently, 
i.e. if you dont need the results until the step, or even entire pipeline is finished dont make a cmd/step endpoint.
```
{
  'run_id': '459d6f9d-bf79-4bcf-b840-f7c3c4fe9362',
  'name': 'fxquants-aep-hello-world',
  'status': 'SUCCESSFUL',
  'commit_changes': False,
  'steps': [
    {
      'step_id': 'd51cb24e-e993-4eb3-8c2d-00f55d87b9f0',
      'run_id': '459d6f9d-bf79-4bcf-b840-f7c3c4fe9362',
      'step_no': 1,
      'name': 'Hello World With Bash',
      'image': 'alpine',
      'status': 'SUCCESSFUL',
      'commit_changes': False,
      'script': [
        {
          'cmd_id': '05a8964d-b8c8-4614-84a2-78490cca5eef',
          'step_id': 'd51cb24e-e993-4eb3-8c2d-00f55d87b9f0',
          'cmd_no': 1,
          'instruction': 'echo Hello World',
          'output': [
            'Hello World\r\n'
          ]
        }
      ]
    }
  ]
}
```

## Getting Started
The first thing that is needed is a Git repository with an fxq-pipeline.yml file present.
See the following example [hello world](https://bitbucket.org/fxquants/aep-hello-world)

## Installing
I highly recommend using the official docker image for this and running the container with the Docker socket
passed into it.

When running the image a gunicorn config with defaults is loaded by the gunicorn cli, its pulled from ```/etc/fxq/ae-runner/gunnicorn.py```
 simply replace this file at runtime to provide custom config.
See Gunicorn Documentation for further information on these Variables:   
http://docs.gunicorn.org/en/stable/settings.html
```
docker run -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock --name ae-runner fxquants/ae-runner:latest
``` 
Alternatively it can be run as a standalone application on the host itself.
I Highly recommend using PIPX to install the FXQuants Runner if installed locally to ensure you do not run into issues 
with other environments and CLI apps installed using PIP 
https://packaging.python.org/guides/installing-stand-alone-command-line-tools/

```
pipx install fxq-ae-runner
```

The standard CLI version is only a development server. I would't use this in production but it may also be fine for
most people. The Docker image version runs the application using Gunicorn and is the only supported production mode.
To run it yourself using Gunicorn perform the following once installed using pip.   
NOTE: It goes without saying if you use pipx to install the fxq-ae-runner, that install is in an isolated venv so you need to get gunicorn installed into that environment.
```
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 fxq.ae.runner.wsgi --log-level info
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