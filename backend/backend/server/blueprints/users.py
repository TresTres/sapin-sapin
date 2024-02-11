from flask import Blueprint, request, make_response, Response, current_app
from flask_restful import Api, Resource, abort
import jwt
import datetime
import typing


from backend.models import *
from backend.db import db
from backend.server.logging import logger

users_blueprint = Blueprint("users", __name__)
users_api = Api(users_blueprint)


class UserRegistration(Resource):
    """
    A resource for registering users.
    """

    def post(self) -> Response:
        """
        Create a new user using the information in the request
        """
        with db.atomic():
            try:
                user = User.create(
                    username=request.json["username"],
                    email=request.json["email"],
                    password=request.json["password"],
                    date_joined=datetime.datetime.now(),
                )
            except IntegrityError:
                abort(409, message="User already exists")
            except ValidationError as val_error:
                abort(400, message=val_error.message)
            return make_response({"new_user": user.username}, 201)


class UserLogin(Resource):
    """
    A resource for logging in users.
    """

    def to_payload(self, user: typing.Dict) -> typing.Dict:
        """
        Convert a user dictionary to a payload
        """
        if "date_joined" in user:
            user["date_joined"] = user["date_joined"].strftime("%Y-%m-%d %H:%M:%S")
        return user

    def post(self) -> Response:
        """
        Validate if a user's login and password is correct
        """
        with db.atomic():
            try:
                user = User.get(
                    (User.username == request.json["identifier"])
                    | (User.email == request.json["identifier"]),
                    User.is_active == True,
                )
                if user.check_password(request.json["password"]):
                    result_user = user.select(
                        User.username, User.email, User.date_joined
                    ).dicts()[0]
                    # Send a JWT token with 30 minute expiration date
                    access_token = jwt.encode(
                        {
                            "user": user.id, 
                            "exp": datetime.datetime.now(datetime.UTC)
                            + datetime.timedelta(minutes=5),
                        },
                        key=current_app.config["APP_KEY"],
                        algorithm="HS256",
                    )

                    resp = make_response(
                        {
                            "user": self.to_payload(result_user),
                        },
                        200,
                        {"Authorization": f"Bearer {access_token}"},
                    )
                    refresh_token = jwt.encode(
                        {
                            "user": user.id,
                        },
                        key=current_app.config["APP_KEY"],
                        algorithm="HS256",
                    )
                    # TODO: Make the cookie secure and use HTTPS
                    # TODO: Set the cookie to samesite="Strict" if the domain is singular
                    # max-age > expires https://www.rfc-editor.org/rfc/rfc7234#section-5.3
                    resp.set_cookie("refresh_token", refresh_token, httponly=True, max_age=60*30)
                    return resp
                abort(
                    401,
                    message="Incorrect password",
                    headers={"WWW-Authenticate": "Basic realm='Wrong password'"},
                )
            except User.DoesNotExist:
                abort(
                    401,
                    message="Could not find user with that username or email",
                    headers={"WWW-Authenticate": "Basic realm='Valid login required'"},
                )
