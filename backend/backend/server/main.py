from flask import Flask
from backend.models import * 


app = Flask(__name__)



@app.before_request
def _db_connect() -> None:
    sql_db.connect()
    
@app.teardown_request
def _db_close(exc: Exception) -> None:
    if not sql_db.is_closed():
        sql_db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user")
def create_user():
    pass 
