PY=python

install:
	$(PY) -m pip install -U pip
	pip install -r requirements.txt

test:
	- rm -rf reports/allure-results
	behave -f pretty -o stdout -f allure -o reports/allure-results

report:
	@echo "Para abrir Allure localmente:"
	@echo "1) Instale o Allure CLI (https://docs.qameta.io/allure/)"
	@echo "2) allure serve reports/allure-results"

docker-build:
	docker build -t python-behavior-api:latest .

docker-test:
	docker run --rm --env-file .env python-behavior-api:latest

ci: install test
