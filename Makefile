# Makefile

.PHONY: uvicorn test

uvicorn:
	uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000

r:
	pip install -r requirements.txt

venv:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; else echo ".venv already exists"; fi

test:
	pytest tests/