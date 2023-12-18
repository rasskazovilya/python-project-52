install:
	poetry install

# start:
# 	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi:application