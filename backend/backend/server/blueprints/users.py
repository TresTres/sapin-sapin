import jwt
import secrets
import hashlib
import datetime
from functools import wraps
from flask import Blueprint, request, make_response, Response, current_app
from flask_restful import Api, Resource, abort
from flask_cors import cross_origin


from backend.models import *
from backend.db import db
from backend.server.logging import logger

users_blueprint = Blueprint("users", __name__)
users_api = Api(users_blueprint)


def jwt_authenticated(f: typing.Callable) -> typing.Callable:
    """
    Decorator to check if a user is authenticated using JWT by checking the Authorization header.
    The request object must be reachable.
    """

    @wraps(f)
    def decorated(*args, **kwargs) -> typing.Callable:
        token = request.headers.get("Authorization")
        if not token:
            abort(
                401,
                message="No token provided",
                headers={"WWW-Authenticate": "Basic realm='Valid login required'"},
            )
        try:
            payload = jwt.decode(
                token,
                key=current_app.config["ACCESS_KEY_SECRET"],
                algorithms=["HS256"],
            )
            user_id = payload["user"]
            # TODO: Implement a check against cookie for fingerprint once https is working
            # if payload["fingerprint"] != request.cookies.get("additional_token"):
            #     abort(401, message="Invalid token")
        except jwt.ExpiredSignatureError:
            abort(401, message="Token has expired, re-login is required.")
        except jwt.InvalidTokenError:
            abort(401, message="Invalid token")
        return f(*args, **kwargs, user_id=user_id)

    return decorated


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
                abort(400, message=val_error.message)
            return make_response({"new_user": user.username}, 201)


class UserLogin(Resource):
    """
    A resource for logging in users.
    """

    def generate_token(self, user: User, fingerprint: str) -> str:
        """
        Generate a JWT token with a 15 minute expiration period for an authenticated user
        """
        # generate a hash of the user's fingerprint
        digest = hashlib.sha256(fingerprint.encode()).hexdigest()
        return jwt.encode(
            {
                "user": user.id,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=15),
                "fingerprint": digest,
            },
            key=current_app.config["ACCESS_KEY_SECRET"],
            algorithm="HS256",
            headers={"typ": "JWT"},
        )

    @cross_origin()
    @jwt_authenticated
    def get(self, user_id: int) -> Response:
        """
        Get the user's information
        """
        with db.atomic():
            user = (
                User.select(User.username, User.email, User.date_joined)
                .where(User.id == user_id)
                .dicts()[0]
            )
            if not user:
                abort(404, message="User not found")
            return make_response(
                {
                    "user": user,
                },
                200,
            )

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
                    result_user = user.select(
                        User.username, User.email, User.date_joined
                    ).dicts()[0]
                    fingerprint = secrets.token_urlsafe(32)
                    access_token = self.generate_token(user, fingerprint)
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
                    # TODO: Harden this cookie and use secure rules for the cookie, label it as __Secure-Fgp
                    # and specify a domain
                    # See https://datatracker.ietf.org/doc/html/draft-west-cookie-prefixes#section-3.1
                    # resp.set_cookie("additional_token", fingerprint, httponly=True, samesite="Strict", secure=True, max_age=60*15)
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
