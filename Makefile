.PHONY: mongotest
mongotest:
	docker run --name mongotest -p 27017:27017 -d mongo:latest

.PHONY: clean
clean:
	pyclean .
