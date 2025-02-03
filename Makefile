
.PHONY: runserver
runserver:
	python crowd_checker/manage.py runserver

.PHONY: makemigrations
makemigrations:
	python crowd_checker/manage.py makemigrations

.PHONY: migrate
migrate:
	python crowd_checker/manage.py migrate
