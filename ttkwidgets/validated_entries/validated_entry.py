"""
Author: Dogeek
License: GNU GPLv3
Source: This repository

ValidatedEntry widget using validators to check the input against specific patterns.
"""

import tkinter.ttk as ttk

from .validators import Validator


class ValidatedEntry(ttk.Entry):
    """
    ValidatedEntry base class.
    An entry that has a VALIDATOR class attribute.
    Set it to a validator class from `ttkwidgets.validated_entries.validators`

    The entry won't accept input that has not been validated.
    """
    VALIDATOR = None

    def _get_validator(self, validator=None):
        """
        Gets a validator instance from either the VALIDATOR class attribute
        or the validator keyword argument.

        :keyword validator: defaults None. A Validator class or instance.
        :type validator: `ttkwidgets.validated_entries.validators.Validator`, `type`
        :raises: TypeError if the validator is None, or is not of type `Validator`
        :returns: a Validator instance
        :rtype: `ttkwidgets.validated_entries.validators.Validator`
        """

        validator = validator or self.VALIDATOR
        if validator is None:
            raise TypeError('No validator found.')

        if isinstance(validator, type):
            validator = validator()

        if not isinstance(validator, Validator):
            raise TypeError("Variable `validator` doesn't have type 'Validator'")
        return validator

    def configure_validator(self, validator=None):
        """
        Configures the validator on this entry. See `ValidatedEntry._get_validator`
        for more info.
        """
        existing_config = {k: self.config(k)[-1] for k in ('validate', 'validatecommand')}

        validator = self._get_validator(validator)
        new_config = validator.validate(self)
        new_config.update(existing_config)
        self.config(new_config)
