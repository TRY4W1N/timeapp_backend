.PHONY: mongotestcontainer
mongotestcontainer:
	docker run --name mongotest -p 27017:27017 -d mongo:latest

.PHONY: mongotest
mongotest:
	docker start mongotest

.PHONY: envbuild
envbuild:
	python3.11 -m venv venv
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: envupdate
envupdate:
	pip install -r requirements.txt

.PHONY: clean
clean:
	pyclean .

.PHONY: lint
lint:
	python -m ruff check .

.PHONY: fmt
fmt:
	python -m isort .
	python -m black .

.PHONY: pre-commit
pre-commit:
	python -m pre-commit run --all-files

.PHONY: testlocal
testlocal:
	python -m pytest src/tests -v

.PHONY: run
run:
	export APP_ENV=DEV & export ENV=LOCAL & python -m src.presentation.http.app

.PHONY: rundocker
rundocker:
	docker compose -f docker-compose.dev.yaml up --build

.PHONY: rundockermetrics
rundockermetrics:
	docker compose -f docker-compose.metrics.yaml up --build