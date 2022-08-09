# todo-api
Simple todo list api created with django rest framework.

## Features
* basic CRUD OPERATIONS
* user token authentication
* swagger auto generated documentation

## Requirements
* docker and docker compose

## Installation
Firstly, clone the repository from the github to your local folder with the following command:
```
git clone https://github.com/pietrykovsky/todo-api.git
```

Next, create an >.env file where the 'docker-compose.yml' is and copy the content from the '.env.sample' file. Example:
```
> '.env' file
DJANGO_SECRET_KEY='example'
DJANGO_ALLOWED_HOSTS=127.0.0.1
DJANGO_DEBUG=True

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
```

In the same directory, where the 'docker-compose.yml' is, run the following commands:
```
docker compose build
docker compose up
```

Now you can head over to http://127.0.0.1:8000/api/docs/

To stop the container run:
```
docker compose down
```