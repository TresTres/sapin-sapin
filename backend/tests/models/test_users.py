import peewee
import pytest

from backend.db import db
from backend.models.users import User
from backend.models.base import ValidationError
from tests.constants import *


class TestUserModel:

    def test_create_user_failure_no_date_joined(self) -> None:
        """
        Test exception when creating a user without a date_joined
        """
        with pytest.raises(peewee.IntegrityError):
            User.create(
                username=VALID_USERNAME,
                email=VALID_EMAIL,
                password=VALID_PASSWORD,
            )

    @pytest.mark.parametrize(
        "username",
        [
            (""),
            ("aaa"),
            ("a" * 36),
            ("a_b_c_d_e"),
            ("9_8_7_6_5"),
            ("aaaa;9999"),
        ],
    )
    def test_create_user_failure_invalid_username_length(self, username: str) -> None:
        """
        Test exception when creating a user with an invalid username:
        - username is empty
        - username is too short
        - username is too long
        - username does not contain a number
        - username does not contain a lowercase letter
        - username contains a disallowed special character
        """
        with pytest.raises(ValidationError):
            User.create(
                username=username,
                email=VALID_EMAIL,
                password=VALID_PASSWORD,
                date_joined=VALID_JOIN_DATE,
            )

    @pytest.mark.parametrize(
        "email",
        [
            (""),
            ("aaa"),
            ("a" * 121),
            ("test_email"),
            ("test_email@"),
            ("test_email@."),
            ("test_email@.com"),
            ("test_email@domain"),
            ("test_email@domain."),
            ("@domain.com"),
            ("test_email@domain.324"),
            ("test_email@domain.f"),
        ],
    )
    def test_create_user_failure_invalid_email(self, email: str) -> None:
        """
        Test exception when creating a user with an invalid email:
        - email is empty
        - email is too short
        - email is too long
        - email does not contain @
        - email does not contain .
        - email does not contain a valid domain
        - email does not contain a valid tld
        - email does not contain a valid name
        """
        with pytest.raises(ValidationError):
            User.create(
                username=VALID_USERNAME,
                email=email,
                ppassword=VALID_PASSWORD,
                date_joined=VALID_JOIN_DATE,
            )

    @pytest.mark.parametrize(
        "password",
        [
            ("aaa"),
            ("a" * 41),
            ("asdfasasdf"),
            ("asdfasas342"),
            ("ASFASFASDFS32423"),
            ("asdfasas342ASDFASDF"),
            ("2ASDFASDF!"),
            ("asdas!43442"),
            ("test_password"),
            ("Test-Password1"),
            ("Test;Password2!"),
            ("Test Password2!"),
            ("testpassword!"),
            ("TESTPASSWORD!"),
            ("TestPassword123"),
        ],
    )
    def test_create_user_failure_invalid_password_length(self, password) -> None:
        """
        Test exception when creating a user without a password:
        - password is too short
        - password is too long
        - password does not contain a number
        - password does not contain a lowercase letter
        - password does not contain an uppercase letter
        - password does not contain a special character
        - password contains a disallowed special character
        """
        with pytest.raises(ValidationError):
            User.create(
                username=VALID_USERNAME,
                email=VALID_EMAIL,
                password=password,
                date_joined=VALID_JOIN_DATE,
            )

    def test_create_user_success(self) -> None:
        """
        Test successful user creation.
        """
        User.create(
            username=VALID_USERNAME,
            email=VALID_EMAIL,
            password=VALID_PASSWORD,
            date_joined=VALID_JOIN_DATE,
        )

        assert User.select().count() == 1
        db_user = User.select().first()
        assert db_user.username == VALID_USERNAME
        assert db_user.email == VALID_EMAIL
        assert db_user.password.startswith("$2b$12$")
        assert db_user.date_joined == VALID_JOIN_DATE
        assert db_user.is_active == True
