PORT ?= 8000

install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager:application

test:
	poetry run manage.py test

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations

setup: migrate install
