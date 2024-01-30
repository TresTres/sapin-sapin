# bin/bash

LOGGING_LEVEL=DEBUG DATABASE_URL=./sqlite/core.db PORT=8000 HOST='localhost' gunicorn backend.server.wsgi:app --reload 