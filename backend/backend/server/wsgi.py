"""
WSGI config for server project.
This will prevent gunicorn from conflicting with the flask app.
"""

import os

from backend.server.main import create_app

APP_MODE = os.environ.get("APP_MODE", "DEV")

app = create_app(APP_MODE)
