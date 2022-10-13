"""
Author: Dogeek
License: GNU GPLv3
Source: This repository

ValidatedEntry widgets for string validation
"""


from string import ascii_lowercase, ascii_uppercase

from .validated_entry import ValidatedEntry
from .validators import (
    EmailValidator, CapitalizedStringValidator,
    PasswordValidator, StringValidator,
    IPv4Validator,
)


class LowerStringEntry(ValidatedEntry):
    """
    Validates only lowercase ascii characters.
    """
    VALIDATOR = StringValidator(ascii_lowercase)


class UpperStringEntry(ValidatedEntry):
    """
    Validates only uppercase ascii characters.
    """
    VALIDATOR = StringValidator(ascii_uppercase)


class CapitalizedStringEntry(ValidatedEntry):
    """
    Validates only capitalized strings (Starts with a capital letter, then any character)
    """
    VALIDATOR = CapitalizedStringValidator


class EmailEntry(ValidatedEntry):
    """
    Validates email addresses.
    """
    VALIDATOR = EmailValidator


class PasswordEntry(ValidatedEntry):
    """
    Validates passwords. The requirements are as follows:
        * At least 1 lowercase character
        * At least 1 uppercase character
        * At least 1 digit
        * At least 1 special character (!@#$%^&*)
        * Be at least 8 characters long
    """
    VALIDATOR = PasswordValidator


class IPv4Entry(ValidatedEntry):
    """
    Validates IPv4 addresses
    """
    VALIDATOR = IPv4Validator
