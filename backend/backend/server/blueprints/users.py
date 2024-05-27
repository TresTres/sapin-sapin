import jwt
import secrets
import datetime
from flask import Blueprint, request, make_response, Response, current_app
from flask_restful import Api, Resource, abort
from flask_cors import cross_origin
from playhouse.shortcuts import model_to_dict


from backend.models import *
from backend.db import db
from backend.server.logging import logger
from backend.server.auth import generate_refresh_token, generate_access_token

users_blueprint = Blueprint("users", __name__)
users_api = Api(users_blueprint)


class UserRegistration(Resource):
    """
    A resource for registering users.
    """

    @cross_origin()
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
                    date_joined=datetime.datetime.now(datetime.UTC),
                )
            except IntegrityError:
                abort(409, message="User already exists")
            except ValidationError as val_error:
                abort(400, message=val_error.args[0])
            return make_response({"newUser": user.username}, 201)


class UserLogin(Resource):
    """
    A resource for logging in users.
    """

    @cross_origin()
    def post(self) -> Response:
        """
        Validate if a user's login and password is correct.
        A validated user will receive a JWT token and an accompoanying hardened cookie.
        """
        with db.atomic():
            try:
                user: User = User.get(
                    (User.username == request.json["identifier"])
                    | (User.email == request.json["identifier"]),
                    User.is_active == True,
                )
                if user.check_password(request.json["password"]):
                    result_user = model_to_dict(
                        user,
                        recurse=False,
                        fields_from_query=User.select(
                            User.username, User.email, User.date_joined
                        ),
                    )
                    fingerprint = secrets.token_urlsafe(32)
                    access_token = generate_access_token(user, fingerprint)
                    refresh_token = generate_refresh_token(user, fingerprint)
                    resp = make_response(
                        {
                            "user": result_user,
                        },
                        200,
                        {
                            "Authorization": f"Bearer {access_token}",
                            "Access-Control-Expose-Headers": "authorization",
                        },
                    )
                    resp.set_cookie(
                        "refresh_token",
                        refresh_token,
                        httponly=True,
                        samesite="Strict",
                        max_age=60 * 15,
                    )
                    # TODO: Harden this cookie with secure and use secure rules for the cookie,
                    # this cookie will be used to verify fingerprint information in subsequent refreshes
                    # See https://datatracker.ietf.org/doc/html/draft-west-cookie-prefixes#section-3.1
                    # resp.set_cookie("__Secure-Fgp", fingerprint, httponly=True, samesite="Strict", secure=True, max_age=60*15)
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


class UserRefreshToken(Resource):
    """
    A resource for refreshing the access token
    """

    @cross_origin()
    def get(self) -> Response:
        """
        Validate if a user's refresh token is correct.
        A validated user will receive a new access token.
        """
        with db.atomic():
            try:
                refresh_token = request.cookies.get("refresh_token")
                user: User = User.get(
                    id=jwt.decode(
                        refresh_token,
                        key=current_app.config["REFRESH_KEY_SECRET"],
                        algorithms=["HS256"],
                    )["user"]
                )
                fingerprint = secrets.token_urlsafe(32)
                access_token = generate_access_token(user, fingerprint)
                resp = make_response(
                    "Access token refreshed",
                    200,
                    {
                        "Authorization": f"Bearer {access_token}",
                        "Access-Control-Expose-Headers": "authorization",
                    },
                )
                return resp
            except jwt.ExpiredSignatureError as ese:
                logger.error(f"Refresh token has expired: {ese}")
                abort(
                    401,
                    message="Refresh token has expired, re-login is required",
                )
            except jwt.InvalidTokenError as ite:
                logger.error(f"Invalid refresh token: {ite}")
                abort(
                    401,
                    message="Invalid refresh token",
                )
            except User.DoesNotExist:
                logger.error("User does not exist")
                abort(401, message="User in refresh token does not exist")
