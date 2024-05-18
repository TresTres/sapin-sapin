from collections import defaultdict
from typing import Dict, List
from flask import Blueprint, request, make_response, Response
from flask_restful import Api, Resource, abort
from flask_cors import cross_origin
from playhouse.shortcuts import model_to_dict

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
                related_events = DataEvent.select().join(DataEventSeries).where(
                    DataEventSeries.owner == user
                )
                events_by_series = defaultdict(list)
                for event in related_events:
                    events_by_series[event.series_id].append(model_to_dict(event, recurse=False))

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
                            "events": events_by_series[s.id],
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
            datetime.datetime.fromisoformat(date_str).date()
            if date_str
            else datetime.date.today()
        )
        
    def sanitize_batch(self, batch: List[Dict[str, str]], series_id: int, batch_offset: int) -> Dict: 
        """
        Sanitize the data batch to ensure that all required fields are present.
        This returns an object containing the sanitized data and the collection of errors if 
        any occurred. 
        """
        sanitized_batch = []   
        error_collection = []
        
        for ind, d in enumerate(batch):
            if not d:
                error_collection.append({ "item": ind + batch_offset, "message": "Item was empty", "field": ""})
                continue
            # TODO: replace all this with validation via pydantic
            try: 
                d["series"] = series_id
                d["amount"] = float(d.get("amount", 0.0))
                d["date"] = self.get_date_from_string(d.get("date", ""))
            except ValueError as ve:
                # TODO: collect all applicable errors in a single item, but not with 
                # multiple try-except blocks
                
                if "time data" in str(ve):
                    error_collection.append({ "item": ind + batch_offset, "message": "Date must be in the format YYYY-MM-DD", "field": "date" })
                elif "could not convert string to float" in str(ve):
                    error_collection.append({ "item": ind + batch_offset, "message": "Amount must be a number", "field": "amount" })
                error_collection.append({ "item": ind + batch_offset, "message": str(ve), "field": ""})
                continue
            sanitized_batch.append(d)
        return {
            "sanitized": sanitized_batch,
            "errors": error_collection
        }

    def create_data_in_batch(
        self, series: DataEventSeries, data: List[Dict[str, str]]
    ) -> int:
        """
        Use the source data to create a batch of data associated to the series.
        Returns the number of rows created and any errors that occurred.
        TODO: If I need to unpack data again, conduct validation using pydantic
        """
        inserted_rows = 0
        errors = []
        with db.atomic():
            if data: 
                for batch in chunked(data, 100):
                    try: 
                        batch_result = self.sanitize_batch(batch, series.id, inserted_rows)
                        errors.extend(batch_result["errors"])
                        sanitized_data = batch_result["sanitized"]
                        if not sanitized_data:
                            continue
                        inserted_rows += DataEvent.insert_many(
                            sanitized_data
                        ).as_rowcount().execute()
                    except IntegrityError as ie:
                        errors.append({"message": str(ie)})
                        break
        return {
            "created": inserted_rows,
            "errors": errors
        }

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
                result = self.create_data_in_batch(series, request.json.get("data"))
                if result["created"] == 0:
                    atxn.rollback()
                    abort(400, message="No valid data were provided", batch_errors=result["errors"])
            except DataEventSeries.DoesNotExist:
                atxn.rollback()
                abort(404, message="Series does not exist")
            return make_response(
                result,
                201,
            )#