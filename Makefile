# Makefile

.PHONY: uvicorn test

uvicorn:
	uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000

test:
	pytest tests/