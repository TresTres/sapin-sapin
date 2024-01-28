from flask import Blueprint, request 
from playhouse.shortcuts import model_to_dict
import datetime
import typing 

from backend.db import sql_db as db
from backend.models import *

users_blueprint = Blueprint("users", __name__)


@users_blueprint.get("/users")
def get_users():
    users = User.select(User.username, User.email, User.date_joined).where(User.is_active == True)
    if not users:
        return {}
    return [model_to_dict(user) for user in users]
    
    

# @users_blueprint.route("/user/registration", methods=["GET", "POST"])
 
    
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
