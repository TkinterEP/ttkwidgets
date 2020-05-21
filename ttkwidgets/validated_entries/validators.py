"""
Author: Dogeek
License: GNU GPLv3
Source: This repository

Validators to validate entry input.
"""

import re
import sys

from ttkwidgets.utilities import isint, isfloat


class Validator:
    """
    Base validator class

    Specify the VALIDATE_ON class attribute (defaults to 'all') to change
    on which tkinter condition the validation will be done.

    Possibilities are :
        * 'all'
        * 'none'
        * 'focus'
        * 'focusin'
        * 'focusout'
        * 'key'
    """
    VALIDATE_ON = 'all'

    def __init__(self, validate_on=None):
        if validate_on is not None:
            self.VALIDATE_ON = validate_on
        self.widget = None

    def validate(self, widget):
        self.widget = widget
        validatecmd = (widget.register(self._validate), '%P')
        return {'validate': self.VALIDATE_ON, 'validatecommand': validatecmd}

    def _validate(self, value):
        return not value

    @property
    def is_valid(self):
        if self.widget is not None:
            return self._validate(self.widget.get())
        raise ValueError('Widget is not attached to this validator')


class MultiValidator:
    """
    Base class to handle multiple validators attachment.
    """
    def __init__(self, *validators, validate_on='all'):
        """
        :param *validators: Validator instances or classes to attach
        :param validate_on: tkinter condition on which the validation will be done
                            default : 'all', see `help(Validator)` for a list of
                            possible values
        """
        if validate_on not in ('all', 'none', 'focusin', 'focusout', 'focus', 'key'):
            raise ValueError(
                "validate_on is not in ('all', 'none', "
                "'focusin', 'focusout', 'focus', 'key')"
            )
        self.validators = []
        for v in validators:
            if isinstance(v, type):
                v = v()
            if isinstance(v, (MultiValidator, Validator)):
                self.validators.append(v)
            else:
                raise TypeError("One of the provided validators is not a Validator or MultiValidator instance")
        self.validate_on = validate_on
        self.widget = None

    def validate(self, widget):
        self.widget = widget
        validatecmd = (widget.register(self._validate), '%P')
        return {'validate': self.validate_on, 'validatecommand': validatecmd}

    def _validate(self, value):
        raise NotImplementedError()

    @property
    def is_valid(self):
        if self.widget is not None:
            return self._validate(self.widget.get())
        raise ValueError('Widget is not attached to this validator')


class AnyValidator(MultiValidator):
    """
    Validates any attached validators. The input will be deemed valid if and only if
    one of the attached validators deem the value valid.
    """
    def _validate(self, value):
        return any(validator._validate(value) for validator in self.validators)


class AllValidator(MultiValidator):
    """
    Validates all attached validators. The input will be deemed valid if and only if
    all attached validators deem the value valid.
    """
    def _validate(self, value):
        return all(validator._validate(value) for validator in self.validators)


class RegexValidator(Validator):
    """
    A validator that will check against a regular expression stored in the REGEX
    class attribute

    REGEX can either be a re.Pattern or a python string.
    """
    REGEX = None

    def __init__(self, regex=None, **kwargs):
        if regex is not None:
            self.REGEX = regex
        super().__init__(**kwargs)

    def _validate(self, value):
        if not isinstance(value, str):
            raise TypeError('{} is not a string.'.format(value))

        if super()._validate(value):
            return True
        #  isinstance(self.REGEX, re.Pattern) only works on 3.7+
        if re.search(r'(Pattern|SRE_Pattern)', self.REGEX.__class__.__name__):
            return self.REGEX.search(value) is not None
        if isinstance(self.REGEX, str):
            return re.search(self.REGEX, value) is not None
        raise TypeError('{} is not a pattern or a string'.format(self.regex))


class IntValidator(Validator):
    def _validate(self, value):
        if super()._validate(value):
            return True

        return isint(value)


class FloatValidator(RegexValidator):
    REGEX = r'[0-9\.]'


class PercentValidator(Validator):
    def _validate(self, value):
        # percentages can be 0-100 integer
        # float 0-1
        if super()._validate(value):
            return True
        return ((isfloat(value) or isint(value)) and 0 <= float(value) <= 100)


class StringValidator(Validator):
    """
    A validator you have to instanciate with a string containing the
    characters you want in.
    """
    def __init__(self, string):
        """
        :param string: String of allowed characters
        :type string: str
        """
        self.string = string

    def _validate(self, value):
        if super()._validate(value):
            return True
        return all([c in self.string for c in value])


class CapitalizedStringValidator(RegexValidator):
    REGEX = '[{}].*'.format("".join([chr(i) for i in range(sys.maxunicode) if chr(i).isupper()]))


class EmailValidator(RegexValidator):
    VALIDATE_ON = 'focusout'

    REGEX = (
        r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|'
        r'(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
    )


class PasswordValidator(RegexValidator):
    """
    Password validator. The requirements are as follows :
        * At least 1 lowercase character
        * At least 1 uppercase character
        * At least 1 digit
        * At least 1 special character (!@#$%^&*)
        * Be at least 8 characters long
    """
    VALIDATE_ON = 'focusout'

    REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})'


class IPv4Validator(RegexValidator):
    """
    Validates IPv4 addresses. The following are valid:
        * localhost
        * 192.168.0.1
        * localhost:3158
    """
    VALIDATE_ON = 'focusout'

    REGEX = r'^((?:[0-9]{1,3}\.){3}[0-9]{1,3}|localhost)(:\d{2,6})?$'
