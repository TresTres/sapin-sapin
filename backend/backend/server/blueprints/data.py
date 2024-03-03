
from flask import Blueprint, request, make_response, Response
from flask_restful import Api, Resource, abort 
from flask_cors import cross_origin

from backend.server.auth import jwt_authenticated

from backend.models import *
from backend.db import db


data_blueprint = Blueprint("data", __name__)
data_api = Api(data_blueprint)


class DataSeriesManagement(Resource):
    """
    A resource for creating and listing data event series
    """
    
    @cross_origin()
    @jwt_authenticated
    def post(self, user_id: str) -> Response:
        """
        Create a new data event series
        """
        with db.atomic():
            try:
                user = User.get(User.id == user_id)
                series = DataEventSeries.create(
                    owner=user,
                    title=request.json.get("title"),
                    description=request.json.get("description"),
                )
            except User.DoesNotExist:
                abort(404, message="User does not exist")
            except IntegrityError:
                abort(409, message="Series already exists")
            except ValidationError as val_error:
                abort(400, message=val_error.args[0])
            return make_response({"new_series": series.title}, 201)

    @cross_origin() 
    @jwt_authenticated
    def get(self, user_id: str) -> Response:
        """
        List all data event series for the current user
        """
        with db.atomic():
            try:
                user = User.get(User.id == user_id)
                series_by_user = DataEventSeries.select().where(DataEventSeries.owner == user)
            except User.DoesNotExist:
                abort(404, message="User does not exist")
            except ValidationError as val_error:
                abort(400, message=val_error.args[0])
            return make_response(
                {
                    "owned_series": [
                        {"title": s.title, "description": s.description} for s in series_by_user
                    ]
                },
                200
            )
            
        