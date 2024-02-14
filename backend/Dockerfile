
FROM python:3.12.2-slim-bullseye


# Create a user for running the app
RUN useradd -m server_admin

WORKDIR /server

# Install system dependencies
RUN apt-get update && apt-get install -y netcat


# Install poetry
RUN pip install poetry
COPY poetry.lock pyproject.toml /server/



# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev 

# Copy code into working directory.  Expected context: <project root>/backend
COPY . /server
RUN mv /server/config/gunicorn.conf.py /server/gunicorn.conf.py

# Set permissions
RUN chown -R server_admin:server_admin /server
USER server_admin
RUN chmod +x prod_entrypoint.sh


ENTRYPOINT [ "poetry", "run" ]
