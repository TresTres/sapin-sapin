from flask import Config

from backend.server.blueprints import *


def create_resource_path(config: Config, resource: str) -> str:
    """
    Create a resource path for the API
    """
    return f"/v{config.get('API_VERSION', '0.0')}/{resource}"


def register_routes(config: Config) -> None:
    """
    Register routes for the app
    """
    users_api.add_resource(
        UserRegistration, create_resource_path(config, "registration")
    )
    users_api.add_resource(UserLogin, create_resource_path(config, "login"))
    users_api.add_resource(UserRefreshToken, create_resource_path(config, "token"))
    
    data_api.add_resource(
        DataSeriesManagement, create_resource_path(config, "data/series")
    )
        
