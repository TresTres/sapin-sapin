
FROM python:3.12.0-slim-bullseye
WORKDIR /app
# Install poetry
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
# Project initialization:
RUN poetry install --no-interaction --no-ansi --without dev 

# Creating folders, and files for a project:
COPY . /app

ENTRYPOINT [ "poetry", "run" ]

