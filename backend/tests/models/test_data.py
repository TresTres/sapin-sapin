import typing
import peewee
import pytest

from backend.models.base import ValidationError
from backend.models.users import User
from backend.models.data import DataEventSeries, DataEvent

from tests.constants import *


@pytest.fixture(scope="class")
def series_user() -> typing.Generator[User, None, None]:
    """
    Create a user for testing data series.
    """
    return User.create(
        username=VALID_USERNAME,
        email=VALID_EMAIL,
        password=VALID_PASSWORD,
        date_joined=VALID_JOIN_DATE,
    )

@pytest.fixture(scope="class")
def event_series(series_user: User) -> typing.Generator[DataEventSeries, None, None]:
    """
    Create a data series for testing data events.
    """
    return DataEventSeries.create(
        owner=series_user,
        title=SERIES_TITLE,
        description=SERIES_DESCRIPTION,
    )


class TestDataEventSeriesModel:
    
    def test_create_series_failure_no_user(self) -> None:
        """
        Test exception when creating a data series without a user
        """
        with pytest.raises(peewee.IntegrityError):
            DataEventSeries.create(
                title=SERIES_TITLE,
                description=SERIES_DESCRIPTION,
            )
        
        
    def test_create_series_failure_no_title(self, series_user: User) -> None:
        """
        Test exception when creating a data series without a title
        """
        with pytest.raises(ValidationError) as ve:
            DataEventSeries.create(
                owner=series_user,
                description=SERIES_DESCRIPTION,
            )
        assert 'Title must be non-empty' in str(ve)
            
    @pytest.mark.parametrize(
        "title,error",
        [
            ("    ", 'length(title) > 0'),
            ("a" * 200, 'length(title) < 200'),
        ],
    )
    def test_create_series_failure_invalid_title(self, series_user: User, title: str, error: str) -> None:
        """
        Test exception when creating a data series without a title
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataEventSeries.create(
                title=title,
                owner=series_user,
                description=SERIES_DESCRIPTION,
            )
        assert error in str(ie)
    
    def test_create_series_failure_duplicate(self, series_user: User) -> None:
        """
        Test exception when creating a data series that already exists. 
        Titles with the same user must be unique (case-insensitive).
        """
        with pytest.raises(peewee.IntegrityError):
            DataEventSeries.create(
                user=series_user,
                title=SERIES_TITLE,
                description=SERIES_DESCRIPTION,
            )
            DataEventSeries.create(
                user=series_user,
                title=SERIES_TITLE,
                description=SERIES_DESCRIPTION,
            )
            
    
class TestSingularDataEventModel:
    
    
    def test_create_event_failure_no_series(self) -> None:
        """
        Test exception when creating a data event without a series
        """
        with pytest.raises(peewee.IntegrityError):
            DataEvent.create(
                label=DATA_LABEL,
                date=DATA_DATE,
                amount=DATA_AMOUNT,
            )
        
    def test_create_event_failure_no_date(self, event_series: DataEventSeries) -> None:
        """
        Test exception when creating a data event without a date
        """
        with pytest.raises(peewee.IntegrityError):
            DataEvent.create(
                label=DATA_LABEL,
                amount=DATA_AMOUNT,
                series=event_series
            )
        
    @pytest.mark.parametrize(
        "label",
        [
            ("x"),
            (None),
        ],
    )
    def test_create_event_failure_duplicate(self, event_series: DataEventSeries, label: typing.Optional[str]) -> None:
        """
        Test exception when creating a data event that already exists. 
        Events with the same series must be unique (case-insensitive).
        """
        with pytest.raises(peewee.IntegrityError):
            DataEvent.create(
                label=label,
                date=DATA_DATE,
                amount=DATA_AMOUNT,
                series=event_series
            )
            DataEvent.create(
                label=label,
                date=DATA_DATE,
                amount=DATA_AMOUNT,
                series=event_series
            )
 
class TestDataCascade:
        
    def test_cascade_series(self, series_user: User, event_series: DataEventSeries) -> None:
        """
        Test that deleting a series deletes its events
        """
        DataEvent.create(
            label=DATA_LABEL,
            date=DATA_DATE,
            amount=DATA_AMOUNT,
            series=event_series
        )
        assert DataEvent.select().count() == 1
        series_user.delete_instance()
        assert DataEvent.select().count() == 0
        assert DataEventSeries.select().count() == 0