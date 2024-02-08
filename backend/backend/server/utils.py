import os 
import typing 

API_VERSION = f"v{os.getenv('API_VERSION', 'DEV')}"
APP_KEY = os.getenv("APP_KEY", "appsecretkey33")


def create_resource_path(resource: str) -> str:
    """
    Create a resource path for the API
    """
    return f"/api/{API_VERSION}/{resource}"
