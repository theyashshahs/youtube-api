# Youtube API Search

Thhis is a Django, Django Rest Framework and Celery based project for fetching youtube public data based on certain pre-defined parameters.

## Setup

### 1. Docker setup

- Copy the contents of `.env.example` to `.env` for environment variables and add your YOUTUBE API KEY.

- Run below command for docker

```sh
$ docker-compose build --no-cache --build-arg SECRET_KEY="<secret key from .env.example>"
```

- The SECRET KEY is in the `.env.example` file.

- For running all the containers.

```sh
$ docker-compose up
```

- To stop the containers press `Ctrl + C`


### 2. Admin Panel

- Create migrations for Database

```sh
$ docker-compose run web python manage.py migrate
```

- Create a super user for django admin.

```sh
$ docker-compose run web python manage.py createsuperuser
```

- Enter the details for creating the user.

- Once the migrations are done, run the server

```sh
$ docker-compose up
```

- The server will be running on port `8000`.


Hooray! The project setup is complete ✨.


## Testing

For testing the fucntionality of this project

- Run the server

```sh
$ docker-compose up
```

### 1. Testing the API

```json
GET /videos/
```

This will provide all the youtube results with cursor pagination sorted in descending order of the published datetime.

### 2. Searching in the API

```json
GET /videos/?q=
```

Write the text you want to search after `?q=`, the searching will take place based on title and description.

This is an optimised searching using Trigram similarity, search rank and search vector.

### 3. Fetching data from YOUTUBE

- Celery task is running every 20 seconds to fetch the data from youtube API and storing the results in database.

### 4. Dashboard for viewing stored data

- If you are running it on local machine then go to `http://127.0.0.1:8000/admin/`
- Enter the user credential you created while setting up the project.
- You will see `Youtubes` in the admin panel which has all the data with searching based on title and youtube video ID.
