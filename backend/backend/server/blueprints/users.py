import jwt
import secrets
import hashlib
import datetime
from flask import Blueprint, request, make_response, Response, current_app
from flask_restful import Api, Resource, abort
from flask_cors import cross_origin


from backend.models import *
from backend.db import db

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
            return make_response({"new_user": user.username}, 201)


class UserLogin(Resource):
    """
    A resource for logging in users.
    """

    def generate_access_token(self, user: User, fingerprint: str) -> str:
        """
        Generate a JWT token with a 1 minute expiration period for an authenticated user
        """
        # generate a hash of the user's fingerprint
        digest = hashlib.sha256(fingerprint.encode()).hexdigest()
        return jwt.encode(
            {
                "user": user.id,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=1),
                "fingerprint": digest,
            },
            key=current_app.config["ACCESS_KEY_SECRET"],
            algorithm="HS256",
            headers={"typ": "JWT"},
        )
        
    def generate_refresh_token(self, user: User, fingerprint: str) -> str:
        """
        Generate a JWT token with a 15 minute expiration period for an authenticated user
        """
        digest = hashlib.sha256(fingerprint.encode()).hexdigest()
        return jwt.encode(
            {
                "user": user.id, 
                "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15),
                "fingerprint": digest,
            },
            key=current_app.config["REFRESH_KEY_SECRET"],
            algorithm="HS256",
            headers={"typ": "JWT"},
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
                    access_token = self.generate_access_token(user, fingerprint)
                    refresh_token = self.generate_refresh_token(user, fingerprint) 
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
                    resp.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict", max_age=60*15)
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
