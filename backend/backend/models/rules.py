import enum 
from backend.models.base import *   


class Interval(ChoiceEnum):
    """Enum for time interval of a rule"""
    DAYS = 1
    WEEKS = 2
    MONTHS = 3
    YEARS = 4
    

class Operation(ChoiceEnum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    


class SinglularFinancialEvent(BaseModel):
    name = CharField()
    description = CharField()
    date = DateTimeField()
    amount = DecimalField()


class RepeatingFinancialRule(BaseModel):
    
    interval = CharField(choices=Interval.as_choices())
    period = DecimalField(auto_round=True, default=1)
    operation = CharField(choices=Operation.as_choices())
    