import os

DEBUG = True
TESTING = False
DATABASE_URL = os.environ.get("DATABASE_URL", "./sqlite/core.db")
APP_KEY = "appdevsecretkey33"
API_VERSION = "DEV"
LOG_LEVEL = "DEBUG"
