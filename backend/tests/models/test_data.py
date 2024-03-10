import typing
import peewee
import pytest

from backend.models.base import ValidationError
from backend.models.users import User
from backend.models.data import *

from tests.constants import *


@pytest.fixture(scope="function")
def series_user() -> typing.Generator[User, None, None]:
    """
    Create a user for testing data series.
    """
    yield User.create(
        username=VALID_USERNAME,
        email=VALID_EMAIL,
        password=VALID_PASSWORD,
        date_joined=VALID_JOIN_DATE,
    )
    User.delete().execute()


@pytest.fixture(scope="function")
def event_series(series_user: User) -> typing.Generator[DataEventSeries, None, None]:
    """
    Create a data series for testing data events.
    """
    yield DataEventSeries.create(
        owner=series_user,
        title=VALID_SERIES_TITLE,
        description=VALID_SERIES_DESCRIPTION,
    )
    DataEventSeries.delete().execute()


class TestDataEventSeriesModel:

    def test_create_series_failure_no_user(self) -> None:
        """
        Test exception when creating a data series without a user
        """
        with pytest.raises(peewee.IntegrityError):
            DataEventSeries.create(
                title=VALID_SERIES_TITLE,
                description=VALID_SERIES_DESCRIPTION,
            )

    def test_create_series_failure_no_title(self, series_user: User) -> None:
        """
        Test exception when creating a data series without a title
        """
        with pytest.raises(ValidationError) as ve:
            DataEventSeries.create(
                owner=series_user,
                description=VALID_SERIES_DESCRIPTION,
            )
        assert "Title must be non-empty" in str(ve)

    @pytest.mark.parametrize(
        "title,error",
        [
            ("    ", "length(title) > 0"),
            ("a" * 200, "length(title) < 200"),
        ],
    )
    def test_create_series_failure_invalid_title(
        self, series_user: User, title: str, error: str
    ) -> None:
        """
        Test exception when creating a data series with an invalid title
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataEventSeries.create(
                title=title,
                owner=series_user,
                description=VALID_SERIES_DESCRIPTION,
            )
        assert error in str(ie)

    def test_create_series_failure_duplicate(self, series_user: User) -> None:
        """
        Test exception when creating a data series that already exists.
        Titles with the same user must be unique (case-insensitive).
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataEventSeries.create(
                owner=series_user,
                title=VALID_SERIES_TITLE,
                description=VALID_SERIES_DESCRIPTION,
            )
            DataEventSeries.create(
                owner=series_user,
                title=VALID_SERIES_TITLE,
                description=VALID_SERIES_DESCRIPTION,
            )
        assert "UNIQUE constraint failed" in str(ie)

    def test_create_series_success(self, series_user: User) -> None:
        """
        Test creating a data series successfully
        """
        DataEventSeries.create(
            owner=series_user,
            title=VALID_SERIES_TITLE,
            description=VALID_SERIES_DESCRIPTION,
        )

        created_series = DataEventSeries.select()[0]
        assert created_series.title == VALID_SERIES_TITLE.upper()
        assert created_series.description == VALID_SERIES_DESCRIPTION
        assert created_series.owner == series_user

    def test_cascade_series_from_owner(self, series_user: User) -> None:
        """
        Test creating a data series successfully,
        then that deleting the owner deletes the series.
        """
        DataEventSeries.create(
            owner=series_user,
            title=VALID_SERIES_TITLE,
            description=VALID_SERIES_DESCRIPTION,
        )

        series_select = DataEventSeries.select()
        assert series_select.count() == 1
        series_user.delete_instance()
        assert DataEventSeries.select().count() == 0


class TestDataEventModel:

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

    def test_create_event_failure_no_label(self, event_series: DataEventSeries) -> None:
        """
        Test exception when creating a data event without a label
        """
        with pytest.raises(ValidationError) as ve:
            DataEvent.create(date=DATA_DATE, amount=DATA_AMOUNT, series=event_series)
        assert "Label must be non-empty" in str(ve)

    @pytest.mark.parametrize(
        "label,error",
        [
            ("    ", "length(label) > 0"),
            ("a" * 200, "length(label) < 120"),
        ],
    )
    def test_create_event_failure_invalid_label(
        self, event_series: DataEventSeries, label: str, error: str
    ) -> None:
        """
        Test exception when creating a data event with an invalid label
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataEvent.create(
                label=label, date=DATA_DATE, amount=DATA_AMOUNT, series=event_series
            )
        assert error in str(ie)

    def test_create_event_failure_duplicate(
        self, event_series: DataEventSeries
    ) -> None:
        """
        Test exception when creating a data event that already exists.
        Events with the same series must be unique (case-insensitive).
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataEvent.create(
                label=DATA_LABEL,
                date=DATA_DATE,
                amount=DATA_AMOUNT,
                series=event_series,
            )
            DataEvent.create(
                label=DATA_LABEL,
                date=DATA_DATE,
                amount=DATA_AMOUNT,
                series=event_series,
            )
        assert "UNIQUE constraint failed" in str(ie)

    def test_create_event_success(self, event_series: DataEventSeries) -> None:
        """
        Test creating a data event successfully
        """
        DataEvent.create(
            label=DATA_LABEL, date=DATA_DATE, amount=DATA_AMOUNT, series=event_series
        )

        created_event = DataEvent.select()[0]
        assert created_event.label == DATA_LABEL
        assert created_event.date == DATA_DATE
        assert created_event.amount == DATA_AMOUNT
        assert created_event.series == event_series

    def test_cascade_event_from_series(self, event_series: DataEventSeries) -> None:
        """
        Test that deleting a data series deletes its data events
        """
        DataEvent.create(
            label=DATA_LABEL, date=DATA_DATE, amount=DATA_AMOUNT, series=event_series
        )
        assert DataEvent.select().count() == 1
        event_series.delete_instance()
        assert DataEvent.select().count() == 0
        assert DataEventSeries.select().count() == 0


class TestDataRecurrenceModel:

    def test_create_recurrence_failure_no_series(self) -> None:
        """
        Test exception when creating a data recurrence without a series
        """
        with pytest.raises(peewee.IntegrityError):
            DataRecurrence.create(
                label=DATA_LABEL,
                start_date=DATA_DATE,
                interval=DATA_INTERVAL,
            )

    def test_create_recurrence_failure_no_label(
        self, event_series: DataEventSeries
    ) -> None:
        """
        Test exception when creating a data recurrence without a label
        """
        with pytest.raises(ValidationError) as ve:
            DataRecurrence.create(
                start_date=DATA_DATE, interval=DATA_INTERVAL, series=event_series
            )
        assert "Label must be non-empty" in str(ve)

    @pytest.mark.parametrize(
        "label,error",
        [
            ("    ", "length(label) > 0"),
            ("a" * 200, "length(label) < 120"),
        ],
    )
    def test_create_recurrence_failure_invalid_label(
        self, event_series: DataEventSeries, label: str, error: str
    ) -> None:
        """
        Test exception when creating a data recurrence with an invalid label
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataRecurrence.create(
                label=label,
                start_date=DATA_DATE,
                interval=DATA_INTERVAL,
                series=event_series,
            )
        assert error in str(ie)

    def test_create_recurrence_failure_start_date_before_end_date(
        self, event_series: DataEventSeries
    ) -> None:
        """
        Test exception when creating a data recurrence with a start date after the end date
        """
        with pytest.raises(ValidationError) as ve:
            DataRecurrence.create(
                label=DATA_LABEL,
                start_date=DATA_DATE,
                end_date=DATA_DATE - datetime.timedelta(days=1),
                interval=DATA_INTERVAL,
                series=event_series,
            )
        assert "Start date must be before end date" in str(ve)

    def test_create_recurrence_failure_duplicate(
        self, event_series: DataEventSeries
    ) -> None:
        """
        Test exception when creating a data recurrence that already exists.
        Recurrences with the same series must be unique (case-insensitive).
        """
        with pytest.raises(peewee.IntegrityError) as ie:
            DataRecurrence.create(
                label=DATA_LABEL,
                start_date=DATA_DATE,
                interval=DATA_INTERVAL,
                series=event_series,
            )
            DataRecurrence.create(
                label=DATA_LABEL,
                start_date=DATA_DATE,
                interval=DATA_INTERVAL,
                series=event_series,
            )
        assert "UNIQUE constraint failed" in str(ie)

    def test_create_recurrence_success(self, event_series: DataEventSeries) -> None:
        """
        Test creating a data recurrence successfully
        """
        DataRecurrence.create(
            label=DATA_LABEL,
            start_date=DATA_DATE,
            interval=DATA_INTERVAL,
            series=event_series,
        )

        created_recurrence = DataRecurrence.select()[0]
        assert created_recurrence.label == DATA_LABEL
        assert created_recurrence.start_date == DATA_DATE
        assert created_recurrence.interval == DATA_INTERVAL
        assert created_recurrence.series == event_series

    def test_cascade_series(self, event_series: DataEventSeries) -> None:
        """
        Test that deleting a series deletes its data recurrences
        """
        DataRecurrence.create(
            label=DATA_LABEL,
            start_date=DATA_DATE,
            interval=DATA_INTERVAL,
            series=event_series,
        )
        assert DataRecurrence.select().count() == 1
        event_series.delete_instance()
        assert DataRecurrence.select().count() == 0
        assert DataEventSeries.select().count() == 0
