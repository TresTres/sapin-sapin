import os

DEBUG = False
TESTING = False
DATABASE_URL = os.environ.get("DATABASE_URL", "/app/sqlite/prod_core.db")
APP_KEY = "appprodsecretkey33"
API_VERSION = "0.0"
LOG_LEVEL = "INFO"
