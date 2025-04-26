
.PHONY: runserver
runserver:
	poetry run python crowd_checker/manage.py runserver

.PHONY: makemigrations
makemigrations:
	poetry run python crowd_checker/manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python crowd_checker/manage.py migrate
