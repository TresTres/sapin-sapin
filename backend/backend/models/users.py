import bcrypt
import re
from peewee import *
from backend.models.base import *


class Currency(ChoiceEnum):
    USD = "$"
    EUR = "€"


class Config(BaseModel):
    """A model for storing configuration values"""

    currency = CharField(choices=Currency.as_choices(), default=Currency.USD)


class User(BaseModel):
    username = CharField(
        unique=True,
        constraints=[Check("length(username) > 5"), Check("length(username) < 35")],
    )
    email = CharField(
        unique=True,
        constraints=[Check("length(email) > 3"), Check("length(email) < 120")],
    )
    password = CharField(
        null=False,
        constraints=[Check("length(password) > 6"), Check("length(password) < 255")],
    )
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(null=False)

    email_regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    password_regex = re.compile(
        r"(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9]){6,40}"
    )

    def validate_email(self, email: str) -> bool:
        """Check if an email is valid for user"""
        if self.email_regex.match(email):
            return True
        return False

    def validate_password(self, password: str) -> bool:
        """Check if a password is valid for user"""
        if self.password_regex.match(password):
            return True
        return False

    def generate_password_hash(self, password: str) -> str:
        """Generate a password hash"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password: str) -> bool:
        """Check a password against the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def save(self, *args, **kwargs) -> int:
        """Override the save method to conduct validations"""
        self.email = self.email.lower()
        self.username = self.username.lower()
        
        if not self.validate_email(self.email):
            raise ValidationError(
                "Email is invalid, must follow format: <name>@<domain>.<tld>"
            )

        if not self.validate_password(self.password):
            raise ValidationError(
                "Password is invalid, must be have a length between 6 and 40 characters and contain at least 1 uppercase, 1 lowercase, 1 number, and 1 special character",
            )
        self.password = self.generate_password_hash(self.password)
        return super().save(*args, **kwargs)
