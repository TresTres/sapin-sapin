import os 
import typing 

API_VERSION = f"v{os.getenv('API_VERSION', 'DEV')}"


def create_resource_path(resource: str) -> str:
    """
    Create a resource path for the API
    """
    return f"/api/{API_VERSION}/{resource}"



ResponseTuple = typing.Tuple[typing.Dict, int]
