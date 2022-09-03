FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PIPENV_VERBOSITY -1
ENV PIPENV_VENV_IN_PROJECT 1

WORKDIR /code

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pipenv pip
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --deploy --dev

COPY app /code/app/
COPY tests /code/tests/

CMD ["uvicorn",  "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000
