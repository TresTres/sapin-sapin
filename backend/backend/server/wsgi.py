"""
WSGI config for server project.
This will prevent gunicorn from conflicting with the flask app.
"""

from backend.server.main import create_app

app = create_app()
