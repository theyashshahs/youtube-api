# Youtube API Search
Thhis is a Django, Django Rest Framework and Celery based project for fetching youtube public data based on certain pre-defined parameters.

## Setup

### 1. Docker setup

- Copy the contents of `.env.example` to `.env` for environment variables and add your YOUTUBE API KEY.

- Run below command for docker
```sh
$ docker-compose build --no-cache --build-arg SECRET_KEY="<secret key from .env>"
```
- The SECRET KEY is in the `.env.example` file.

- For running all the containers. 
```sh
$ docker-compose up
```

### 2. Admin Panel
- Create a super user for django admin.

```sh
$ docker-compose run web python manage.py createsuperuser
```
- Enter the details for creating the user.

- Run
```sh
$ docker-compose up
```

Browse port `8000` for server.


Hooray! the project setup is complete ✨.
