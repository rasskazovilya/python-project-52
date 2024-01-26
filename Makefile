PORT ?= 8000

install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

test:
	poetry run python manage.py test

lint:
	poetry run flake8 .

test-lint: test lint

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations

setup: 
	./build.sh
