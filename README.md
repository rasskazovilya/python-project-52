### Hexlet tests and linter status:
[![Actions Status](https://github.com/rasskazovilya/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/rasskazovilya/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/61b8cb48e1e16fa01194/maintainability)](https://codeclimate.com/github/rasskazovilya/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/61b8cb48e1e16fa01194/test_coverage)](https://codeclimate.com/github/rasskazovilya/python-project-52/test_coverage)


[Link](https://hexlet-task-manager-qtt4.onrender.com)

## Task Manager
Task manager is a final educational project from Hexlet Python Developer course. It as a Django application for managing tasks with different statuses and labels. The app handles user authetication so only registered and logged in users can create, change or delete entities (CRUD). The app uses PostgreSQL as database, Bootstrap5 and Django templates for simple frontend and Django with django-filters for backend.

### Requirements
- python >= 3.8.1
- django >=3.2.3, <4.1
- django-bootstrap >= 23.3
- django-filter >= 23.5

Others are listed in requirements.txt or pyproject.toml.  

Django should not be higher than 4.1 because my potato computer can not handle higher versions. There is also a chance that for a higher version of Django the logout view would not work properly because of GET method not working with basic LogoutView for safety reasons.

### Installation
- Clone this repo  
```
git clone https://github.com/rasskazovilya/python-project-52
```
- Go to repo directory  
```
cd python-project-52
```
- Install application  
```
make setup
```

### Usage
Run app locally:
```
make dev
```

Run tests:
```
make test
```

Run app on server:
```
make start
```