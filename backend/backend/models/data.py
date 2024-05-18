import datetime
import decimal
import uuid

from backend.models.base import *
from backend.models.users import User


class TimeDeltaField(DecimalField):
    """
    Represents a time delta in seconds.
    """

    field_type = "DECIMAL"

    def db_value(self, value: datetime.timedelta) -> decimal.Decimal:
        """
        Converts value into a database representation

        Args:
            value: The value to convert

        Returns:
            decimal.Decimal: The converted value as a decimal
        """
        return super().db_value(value.total_seconds())

    def python_value(self, value: decimal.Decimal) -> datetime.timedelta:
        """
        Converts value into a python representation for application sue

        Args:
            value: The value to convert

        Returns:
            datetime.timedelta: The converted value
        """
        return datetime.timedelta(seconds=float(super().python_value(value)))


class DataEventSeries(BaseModel):
    """
    Represents a naive collection of events.
    """

    owner = ForeignKeyField(User, on_delete="CASCADE")
    title = CharField(
        null=False,
        constraints=[Check("length(title) > 0"), Check("length(title) < 200")],
    )
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


class DataModel(BaseModel):
    """
    Represents a generic data model.
    """

    label = CharField(
        null=False,
        constraints=[Check("length(label) > 0"), Check("length(label) < 120")],
        default="",
    )
    description = CharField(null=True)
    amount = DecimalField(null=False, decimal_places=4, default=0.0000)
    series = ForeignKeyField(DataEventSeries, on_delete="CASCADE")

    class Meta:
        constraints = [SQL("UNIQUE (series_id, label)")]


class DataEvent(DataModel):
    """
    Represents a single event in a series.
    """

    date = DateTimeField(
        null=False, index=True, default=datetime.datetime.now(datetime.UTC)
    )

    class Meta:
        indexes = ((("series", "label", "date"), True),)

    def save(self, *args, **kwargs) -> int:
        """
        Override the save method to conduct validations.
        Label must be non-empty
        """
        if not self.label or len(self.label.strip()) == 0:
            # TODO: If I ever need to do this again, refactor it to a util
            random_id = uuid.uuid4()
            sanitized_series_tile = self.series.title.lower().replace(" ", "-")
            self.label = f"{sanitized_series_tile}-event-{random_id}"

        self.label = self.label.strip()
        return super().save(*args, **kwargs)


class DataRecurrence(BaseModel):
    """
    Represents an event that reoccurs on a schedule.
    """

    label = CharField(
        null=False,
        constraints=[Check("length(label) > 0"), Check("length(label) < 120")],
        default="",
    )
    description = CharField(null=True)
    start_date = DateTimeField(
        null=False, index=True, default=datetime.datetime.now(datetime.UTC)
    )
    end_date = DateTimeField(null=True)
    interval = TimeDeltaField(null=False, decimal_places=5, default=1)
    amount = DecimalField(null=False, decimal_places=4, default=0.0000)
    series = ForeignKeyField(DataEventSeries, on_delete="CASCADE")

    class Meta:
        constraints = [SQL("UNIQUE (series_id, label)")]
        indexes = ((("series", "start_date", "label"), True),)

    def save(self, *args, **kwargs) -> int:
        """
        Override the save method to conduct validations.
        """
        if not self.label:
            raise ValidationError("Label must be non-empty")
        self.label = self.label.strip()
        if self.end_date and self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")
        return super().save(*args, **kwargs)
