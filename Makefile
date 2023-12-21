install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi:application