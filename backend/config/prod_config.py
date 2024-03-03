import os

DEBUG = False
TESTING = False
DATABASE_URL = os.environ.get("DATABASE_URL", "/server/sqlite/prod_core.db")
ACCESS_KEY_SECRET = "prodsecretkey33"
REFRESH_KEY_SECRET = "prodrefreshkey43"
API_VERSION = "0.0"
LOG_LEVEL = "INFO"
