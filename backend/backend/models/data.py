from backend.models.base import *
from backend.models.users import User


class DataEventSeries(BaseModel):
    """
    Represents a series of events.
    """
    owner = ForeignKeyField(User, on_delete="CASCADE")
    title = CharField(null=False, constraints=[Check("length(title) > 0"), Check("length(title) < 200")])
    description = CharField(null=True)
    
    class Meta:
        constraints = [SQL("UNIQUE (owner_id, title)")]
    
    def save(self, *args, **kwargs) -> int:
        """
        Override the save method to conduct validations.  
        Title must be non-empty and will be converted to uppercase.
        """
        if not self.title:
            raise ValidationError("Title must be non-empty")
        self.title = self.title.strip().upper()
        return super().save(*args, **kwargs)
    

class DataEvent(BaseModel):
    """
    Represents a single event in a series.
    """
    label = CharField(null=False, constraints=[Check("length(label) < 120")], default="")
    description = CharField(null=True)
    date = DateTimeField(null=False)
    amount = DecimalField(null=False, decimal_places=4, default=0.0000)
    series = ForeignKeyField(DataEventSeries, on_delete="CASCADE")
    
    class Meta:
        constraints = [SQL("UNIQUE (series_id, date, label)")]