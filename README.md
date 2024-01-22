### What is this repository for? ###

This is the python repo for university service.
There are 2 major components to this:

* Flask App: REST APIs
* Worker: Celery Workers for Async Tasks

### How do I get set up? ###

#### Local

Create & Activate a Virtual Environment

```commandline
sudo pip install virtualenv
virtualenv ~/Projects/venv/logisticsnow-env -p python3.8.3
source ~/Projects/venv/logisticsnow-env/bin/activate
```

Installing Requirements

```commandline
pip install -r requirements.txt
```

Start the Flask Application

```commandline
ENVIRONMENT='development' python app/flask_app.py
```

#### Local Docker

```commandline
docker-compose -f build
docker-compose up
```

### How to run tests

Install The App as a python package

```commandline
pip install -e .
```

Run the Tests

```commandline
pytest
```

̄
Get the coverage Report

```commandline
coverage run -m pytest
coverage report
```

