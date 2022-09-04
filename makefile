# Run docker containers detached
.PHONY: run
run:
	docker-compose down --remove-orphans && \
	docker-compose up --build -d

# Attach to docker containers
.PHONY: attach
attach:
	docker-compose up

ARGPATH="tests"
.PHONY: test
test:
	docker-compose up -d  && \
	docker exec -it optom-api-app sh -c "pytest -vv -k $(ARGPATH) --cov-report html --cov='app'"

.PHONY: tox
tox:
	docker-compose up -d  && \
	docker exec -it optom-api-app sh -c "tox"

.PHONY: install
install:
	pre-commit install && \
	pre-commit autoupdate && \
	pipenv install --skip-lock --dev

MESSAGE=""
.PHONY: makemigrations
makemigrations:
	docker-compose up -d && \
	docker exec -it optom-api-app alembic revision --autogenerate -m "$(MESSAGE)"

UPGRADE="head"
.PHONY: migrate
migrate:
	docker-compose up -d && \
	docker exec -it optom-api-app alembic upgrade "$(UPGRADE)"
