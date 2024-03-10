from flask import Config

from backend.server.blueprints import *
from backend.server.blueprints.utils import create_resource_path

def register_routes(config: Config) -> None:
    """
    Register routes for the app
    """
    users_api.add_resource(
        UserRegistration, create_resource_path(config, "registration")
    )
    users_api.add_resource(UserLogin, create_resource_path(config, "login"))
    users_api.add_resource(UserRefreshToken, create_resource_path(config, "me/refresh"))
    
    data_api.add_resource(
        DataSeriesManagement, create_resource_path(config, "data/series")
    )
        
