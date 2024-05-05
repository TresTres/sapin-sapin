from typing import Dict, List, ContextManager
from flask import Blueprint, request, make_response, Response
from flask_restful import Api, Resource, abort
from flask_cors import cross_origin

from backend.server.auth import jwt_authenticated

from backend.models import *
from backend.db import db


data_blueprint = Blueprint("data", __name__)
data_api = Api(data_blueprint)


class DataSeries(Resource):
    """
    A resource for creating and listing data event series
    """

    @cross_origin()
    @jwt_authenticated
    def post(self, user_id: str) -> Response:
        """
        Create a new data event series
        """
        with db.atomic() as atxn:
            try:
                user = User.get(User.id == user_id)
                series = DataEventSeries.create(
                    owner=user,
                    title=request.json.get("title"),
                    description=request.json.get("description"),
                )
            except User.DoesNotExist:
                atxn.rollback()
                abort(404, message="User does not exist")
            except IntegrityError:
                atxn.rollback()
                abort(409, message="Series already exists")
            except ValidationError as val_error:
                atxn.rollback()
                abort(400, message=val_error.args[0])
            return make_response(
                {
                    "id": series.id,
                    "title": series.title,
                    "description": series.description,
                },
                201,
            )

    @cross_origin()
    @jwt_authenticated
    def get(self, user_id: str) -> Response:
        """
        List all data event series for the current user
        """
        with db.atomic():
            try:
                user = User.get(User.id == user_id)
                series_by_user = DataEventSeries.select().where(
                    DataEventSeries.owner == user
                )
            except User.DoesNotExist:
                abort(404, message="User does not exist")
            except ValidationError as val_error:
                abort(400, message=val_error.args[0])
            return make_response(
                {
                    "owned_series": [
                        {
                            "id": s.id,
                            "title": s.title,
                            "description": s.description,
                            "events": [],
                            "recurrences": [],
                        }
                        for s in series_by_user
                    ]
                },
                200,
            )


class DataBatch(Resource):
    """
    A resource for data resource CRUD
    """

    def get_date_from_string(self, date_str: str) -> datetime.date:
        """
        Convert a string into a date object.
        TODO: If I need to do this again, extract it out to util
        """

        return (
            datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_str
            else datetime.date.today()
        )

    def create_data_in_batch(
        self, txn: ContextManager, series: DataEventSeries, data: List[Dict[str, str]]
    ) -> None:
        """
        Use the source data to create a batch of data associated to the series
        TODO: If I need to unpack data again, conduct validation using pydantic
        """
        for batch in chunked(data, 100):
            DataEvent.insert_many(
                [
                    {
                        "label": d.get("label", ""),
                        "description": d.get("description", ""),
                        "amount": d.get("amount", 0.0),
                        "date": self.get_date_from_string(d.get("date", "")),
                        "series": series,
                    }
                    for d in batch
                ]
            )

    @cross_origin()
    @jwt_authenticated
    def post(self, **kwargs) -> Response:
        """
        Create a batch of data for the specified series
        Absorbs keyword "user_id" as it's not used.
        """

        with db.atomic() as atxn:
            try:
                series = DataEventSeries.get(
                    DataEventSeries.id == request.json.get("series_id")
                )
                self.create_data_in_batch(atxn, series, request.json.get("data"))
                
            except DataEventSeries.DoesNotExist:
                abort(404, message="Series does not exist")
