import os

DEBUG = True
TESTING = False
DATABASE_URL = os.environ.get("DATABASE_URL", "./sqlite/core.db")
ACCESS_KEY_SECRET = "appdevsecretkey33"
REFRESH_KEY_SECRET = "devrefreshkey43"
API_VERSION = "DEV"
LOG_LEVEL = "DEBUG"
