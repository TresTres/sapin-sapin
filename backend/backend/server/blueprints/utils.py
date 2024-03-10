from flask import Config

def create_resource_path(config: Config, resource: str) -> str:
    """
    Create a resource path for the API
    """
    return f"/v{config.get('API_VERSION', '0.0')}/{resource}"