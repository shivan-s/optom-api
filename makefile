# Run docker containers detached
.PHONY: run
run:
	docker-compose down --remove-orphans && \
	docker-compose --env-file '.env' up --build -d

# Attach to docker containers
.PHONY: attach
attach:
	docker-compose up

ARGPATH="tests"
.PHONY: test
test:
	docker-compose --env-file '.env' up -d  && \
	docker exec -it optom-api-app sh -c "pytest -vv -k $(ARGPATH) --cov-report html --cov='app'"

.PHONY: tox
tox:
	docker-compose --env-file '.env' up -d  && \
	docker exec -it optom-api-app sh -c "tox"

.PHONY: install
install:
	pre-commit install && \
	pre-commit autoupdate && \
	pipenv install --skip-lock --dev

MESSAGE=""
.PHONY: makemigrations
makemigrations:
	pipenv run alembic revision --autogenerate -m "$(MESSAGE)"

UPGRADE="head"
.PHONY: migrate
migrate:
	pipenv run alembic upgrade "$(UPGRADE)"
