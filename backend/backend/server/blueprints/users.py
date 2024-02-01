from flask import Blueprint, request
from flask_restful import Api, Resource, abort
from playhouse.shortcuts import model_to_dict
import datetime
import typing

from backend.db import sql_db as db
from backend.models import *
from backend.server.logging import logger
from backend.server.utils import create_resource_path, ResponseTuple

users_blueprint = Blueprint("users", __name__)
users_api = Api(users_blueprint)


class UserRegistration(Resource):
    """
    A resource for registering users.
    """

    def post(self) -> ResponseTuple:
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
            return {"new_user_id": user.id}, 201


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

    def post(self) -> ResponseTuple:
        """
        Validate if a user's login and password is correct
        """
        with db.atomic():
            try:
                user = (
                    User.get(
                        (User.username == request.json["identifier"])
                        | (User.email == request.json["identifier"]),
                        User.is_active == True,
                    )
                    .select(User.username, User.email, User.date_joined)
                    .dicts()
                )
                if user.check_password(request.json["password"]):
                    return {"user": self.to_payload(user)}, 200
                abort(401, message="No password match found")
            except User.DoesNotExist:
                abort(401, message="Could not find user with that username or email")


class AppUser(Resource):
    """
    A resource for retrieving users
    """

    def get(self) -> ResponseTuple:
        users = (
            User.select(User.username, User.email, User.date_joined)
            .where(User.is_active == True)
            .dicts()
        )
        if not len(users):
            return {}, 204

        return {"users": [self.to_payload(user) for user in users]}, 200


users_api.add_resource(UserRegistration, create_resource_path("registration"))
users_api.add_resource(UserLogin, create_resource_path("login"))
users_api.add_resource(AppUser, create_resource_path("users"))

# @users_blueprint.route("/user/registration", methods=["POST"])

# @users_blueprint.post("/user/registration")

# @users_blueprint.post("/register")
# def create_user():
#     with db.atomic():
#         try:
#             user = User.create(
#                 username=request.json["username"],
#                 email=request.json["email"],
#                 password=request.json["password"],
#                 date_joined=datetime.datetime.now(),
#             )
#         except IntegrityError:
#             return {"error": "User already exists"}
#         return user

# @app.route('/join/', methods=['GET', 'POST'])
# def join():
#     if request.method == 'POST' and request.form['username']:
#         try:
#             with database.atomic():
#                 # Attempt to create the user. If the username is taken, due to the
#                 # unique constraint, the database will raise an IntegrityError.
#                 user = User.create(
#                     username=request.form['username'],
#                     password=md5((request.form['password']).encode('utf-8')).hexdigest(),
#                     email=request.form['email'],
#                     join_date=datetime.datetime.now())

#             # mark the user as being 'authenticated' by setting the session vars
#             auth_user(user)
#             return redirect(url_for('homepage'))

#         except IntegrityError:
#             flash('That username is already taken')

#     return render_template('join.html')


# @users_blueprint.post("/create_user")
# def
