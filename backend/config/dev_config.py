import os

DEBUG = True
TESTING = False
DATABASE_URL = os.environ.get("DATABASE_URL", "/app/sqlite/core.db")
ACCESS_KEY_SECRET = "appdevsecretkey33"
REFRESH_KEY_SECRET = "appdevrefreshkey43"
API_VERSION = "DEV"
LOG_LEVEL = "DEBUG"
