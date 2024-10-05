venv:
	python3 -m venv .venv

install: venv
	. ./.venv/bin/activate && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt

up:
	docker-compose up -d

down:
	docker-compose down

start:
	. ./.venv/bin/activate && \
	python ./src/main.py