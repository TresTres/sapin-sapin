#!/bin/bash

# Server entry point which receives the environment variables and starts the server

gunicorn backend.server.wsgi:app