
FROM python:3.12.0-slim-bullseye


# Create a user for running the app
RUN useradd -m server_admin

WORKDIR /app

# Install poetry
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev 

# Copy code into working directory.  Expected context: <project root>/backend
COPY . /app

# Set permissions
RUN chown -R server_admin:server_admin /app
# USER server_admin
RUN chmod +x prod_entrypoint.sh


ENTRYPOINT [ "poetry", "run" ]
