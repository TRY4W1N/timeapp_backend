.PHONY: mongotest
mongotest:
	docker run --name mongotest -p 27017:27017 -d mongo:latest

.PHONY: clean
clean:
	pyclean .

.PHONY: lint
lint:
	python -m ruff .

.PHONY: fmt
fmt:
	python -m isort .
	python -m black .

.PHONY: pre-commit
pre-commit:
	python -m pre-commit run --all-files