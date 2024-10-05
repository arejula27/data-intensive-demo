venv:
	python3 -m venv .venv

install: venv
	. ./.venv/bin/activate && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt

format:
	. ./.venv/bin/activate && \
	black src

up:
	docker-compose up -d

down:
	docker-compose down

# Wait for all services to be up
start:
	. ./.venv/bin/activate && \
	python ./src/main.py