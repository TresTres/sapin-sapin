#!/bin/bash

# Server entry point which receives the environment variables and starts the server

APP_MODE=DEV PORT=8000 HOST='localhost' gunicorn backend.server.wsgi:app --reload