from .validated_entry import ValidatedEntry
from .validators import PercentValidator, IntValidator, FloatValidator


class PercentEntry(ValidatedEntry):
    """
    Validates floats between 0 and 100
    """
    VALIDATOR = PercentValidator


class IntEntry(ValidatedEntry):
    """
    Validates integers (no floating point)
    """
    VALIDATOR = IntValidator


class FloatEntry(ValidatedEntry):
    """
    Validated floating-point numbers.
    """
    VALIDATOR = FloatValidator
