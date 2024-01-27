import abc 
import enum
import typing 
from peewee import *

sql_db = SqliteDatabase('core.db')

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = sql_db
        


class ChoiceEnum(enum.Enum):
    """
    Abstract base class for creating model choice enums
    """
    
    @classmethod
    def as_choices(cls) -> typing.List[typing.Tuple[str, str]]:
        """Return the enum as a list of choices for a Django model field"""
        return [(i.name, i.value) for i in cls]


    
    
    