#!/bin/bash

# Server entry point which receives the environment variables and starts the server

APP_MODE=PROD gunicorn backend.server.wsgi:app