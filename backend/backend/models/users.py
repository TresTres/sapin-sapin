from peewee import *
from backend.models.base import * 

class Currency(ChoiceEnum):
    USD = "$"
    EUR = "€"


class Config(BaseModel):
    """A model for storing configuration values"""
    currency = CharField(choices=Currency.as_choices(), default=Currency.USD)
    


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    is_active = BooleanField(default=True)
    date_joined = DateTimeField()

