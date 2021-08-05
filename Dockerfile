FROM python:3.9.5

WORKDIR /src

COPY . /src

ARG SECRET_KEY
ENV SECRET_KEY ${SECRET_KEY}

RUN apt-get update && \
    apt-get -y install python3-dev libpq-dev musl-dev libssl-dev && \
    pip3 install pipenv setuptools wheel && \
    pipenv lock -r > requirements.txt && \
    pipenv lock --dev -r > dev-requirements.txt && \
    pip3 install -r requirements.txt && \
    python manage.py collectstatic --clear --no-input

EXPOSE 8000
