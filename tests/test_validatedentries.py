# Copyright (c) Dogeek 2020
# For license see LICENSE
import string

import ttkwidgets.validated_entries as v_entries
from tests import BaseWidgetTest
import tkinter as tk


class TestValidatedEntry(BaseWidgetTest):
    def _test_entry_init(self, entry):
        entry = entry(self.window, validate='all')
        entry.configure_validator()
        entry.pack()
        self.window.update()

    def assertValidatedTrue(self, entry_class, inserted):
        entry = entry_class(self.window)
        entry.pack()
        self.window.update()
        validator = entry._get_validator()
        self.assertTrue(validator._validate(inserted))

    def assertValidatedFalse(self, entry_class, inserted):
        entry = entry_class(self.window)
        entry.pack()
        self.window.update()
        validator = entry._get_validator()
        self.assertFalse(validator._validate(inserted))

    def test_validated_entries_init(self):
        entries = [e for e in dir(v_entries) if e.endswith('Entry')]
        for e in entries:
            entry = vars(v_entries)[e]
            if isinstance(entry, v_entries.ValidatedEntry):
                self._test_entry_init(entry)

    def test_intentry_validation(self):
        self.assertValidatedFalse(v_entries.IntEntry, 'abc123')
        self.assertValidatedTrue(v_entries.IntEntry, '123')

    def test_floatentry_validation(self):
        # self.assertValidatedFalse(v_entries.FloatEntry, 'abc123.45')
        self.assertValidatedTrue(v_entries.FloatEntry, '123.45')

    def test_percententry_validation(self):
        self.assertValidatedFalse(v_entries.PercentEntry, '123.56')
        self.assertValidatedFalse(v_entries.PercentEntry, 'aaa')
        self.assertValidatedTrue(v_entries.PercentEntry, '12.56')

    def test_lowerstringentry_validation(self):
        self.assertValidatedFalse(v_entries.LowerStringEntry, 'abc123')
        self.assertValidatedTrue(v_entries.LowerStringEntry, 'abc')

    def test_upperstringentry_validation(self):
        self.assertValidatedFalse(v_entries.UpperStringEntry, 'ABCdef')
        self.assertValidatedTrue(v_entries.UpperStringEntry, 'ABC')

    def test_capitalizedstringentry_validation(self):
        self.assertValidatedTrue(v_entries.CapitalizedStringEntry, 'Abc')
        self.assertValidatedFalse(v_entries.CapitalizedStringEntry, 'abc')

    def test_emailentry_validation(self):
        self.assertValidatedTrue(v_entries.EmailEntry, 'test@example.com')
        self.assertValidatedFalse(v_entries.EmailEntry, 'abcdef')

    def test_passwordentry_validation(self):
        self.assertValidatedTrue(v_entries.PasswordEntry, 'aBc&12345')
        self.assertValidatedFalse(v_entries.PasswordEntry, 'aBc&123')  # Length
        self.assertValidatedFalse(v_entries.PasswordEntry, 'aBc&aaaaa')  # No digits
        self.assertValidatedFalse(v_entries.PasswordEntry, 'abc&12345')  # No cap
        self.assertValidatedFalse(v_entries.PasswordEntry, 'ABC&1234')  # No lowercase
        self.assertValidatedFalse(v_entries.PasswordEntry, 'aBcd1234')  # No special

    def test_validatedentry_no_validator(self):
        entry = v_entries.ValidatedEntry()
        validator = v_entries.Validator
        vinstance = validator()

        with self.assertRaises(TypeError):
            entry._get_validator()

        with self.assertRaises(TypeError):
            entry._get_validator(123)
            entry._get_validator('123')

        self.assertIsInstance(entry._get_validator(validator), v_entries.Validator)
        self.assertIs(entry._get_validator(vinstance), vinstance)

    def test_multi_validator(self):
        with self.assertRaises(TypeError):
            val = v_entries.AllValidator(v_entries.FloatValidator, int)

        self.assertTrue(
            v_entries.AllValidator(
                v_entries.RegexValidator(r'.'),
                v_entries.RegexValidator(r'\d'),
                )._validate('1')
        )
        self.assertFalse(
            v_entries.AllValidator(
                v_entries.RegexValidator(r'[a-z]'),
                v_entries.RegexValidator(r'\d'),
                )._validate('1')
        )

        self.assertTrue(
            v_entries.AnyValidator(
                v_entries.RegexValidator(r'.'),
                v_entries.RegexValidator(r'\d'),
                )._validate('1')
        )
        self.assertTrue(
            v_entries.AnyValidator(
                v_entries.RegexValidator(r'[a-z]'),
                v_entries.RegexValidator(r'\d'),
                )._validate('1')
        )

    def test_regex_validator(self):
        self.assertTrue(v_entries.RegexValidator(r'\d')._validate('1'))
        self.assertTrue(v_entries.RegexValidator(r'[a-z]')._validate('a'))
        self.assertFalse(v_entries.RegexValidator(r'[a-z]')._validate('1'))
        self.assertFalse(v_entries.RegexValidator(r'\d')._validate('a'))

    def test_number_validators(self):
        self.assertTrue(v_entries.FloatValidator()._validate('1.0'))
        self.assertTrue(v_entries.IntValidator()._validate('1'))
        self.assertTrue(v_entries.PercentValidator()._validate('0.55'))
        self.assertFalse(v_entries.PercentValidator()._validate('123'))

    def test_string_validators(self):
        self.assertTrue(v_entries.StringValidator(string.ascii_lowercase)._validate('abc'))
        self.assertFalse(v_entries.StringValidator(string.ascii_lowercase)._validate('ABC'))
        self.assertTrue(v_entries.StringValidator(string.ascii_uppercase)._validate('ABC'))
        self.assertFalse(v_entries.StringValidator(string.ascii_uppercase)._validate('abc'))
        self.assertTrue(v_entries.EmailValidator()._validate('firstname@example.com'))
        self.assertTrue(v_entries.PasswordValidator()._validate('Abcd&1234'))


if __name__ == '__main__':
    import unittest
    unittest.main()
