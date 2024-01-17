install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi:application

test:
	poetry run manage.py test

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations