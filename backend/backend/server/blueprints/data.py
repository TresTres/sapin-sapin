
from flask import Blueprint, request, make_response, Response
from flask_restful import Api, Resource, abort 
from flask_cors import cross_origin

from backend.server.main import jwt_authenticated

from backend.models import *
from backend.db import db


data_blueprint = Blueprint("data", __name__)
data_api = Api(data_blueprint)


class DataSeriesManagement(Resource):
    """
    A resource for creating and listing data event series
    """
    
    @cross_origin
    @jwt_authenticated
    def post(self, user_id: str) -> Response:
        """
        Create a new data event series
        """
        with db.atomic():
            try:
                user = User.get(User.id == user_id)
                if not user: 
                    raise ValidationError("User does not exist")
                series = DataEventSeries.create(
                    owner=user,
                    title=request.json["title"],
                    description=request.json.get("description"),
                )
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
                if not user: 
                    raise ValidationError("User does not exist")
                series_by_user = DataEventSeries.select().where(DataEventSeries.owner == user)
            except ValidationError as val_error:
                abort(400, message=val_error.args[0])
            return make_response(
                {
                    "owned_series": [
                        {"title": s.title, "description": s.description} for s in series_by_user
                    ]
                },
            )
            
        