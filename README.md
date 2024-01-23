# Simple Blog System

This is a simple blog system implemented in Flask, featuring user authentication and CRUD operations for blog posts.

## Database Schema

### User Table

The `User` table stores information about registered users.

| Column      | Type         | Constraints              |
|-------------|--------------|--------------------------|
| id          | Integer      | Primary Key              |
| username    | String(80)   | Unique, Not Null         |
| password    | String(255)  | Not Null                 |
| created_at  | DateTime     | Default: current time    |
| modified_at | DateTime     | Default: current time    (on update) |

### BlogPost Table

The `BlogPost` table stores information about individual blog posts.

| Column      | Type         | Constraints              |
|-------------|--------------|--------------------------|
| id          | Integer      | Primary Key              |
| title       | String(255)  | Not Null                 |
| content     | Text         | Not Null                 |
| author      | String       | Not Null                 |
| created_at  | DateTime     | Default: current time    |
| modified_at | DateTime     | Default: current time    (on update) |

The `author_id` column in the `BlogPost` table references the `id` column in the `User` table, creating a relationship between users and their blog posts.


### How do I get set up? ###

#### Local ####

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

