# Copyright (c) RedFantom 2017
# For license see LICENSE
import ttkwidgets.validated_entries as v_entries
from tests import BaseWidgetTest
import tkinter as tk


class TestScaleEntry(BaseWidgetTest):
    def _test_entry_init(self, entry):
        entry = entry(self.window)
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

    def test_entries_init(self):
        entries = [e for e in dir(v_entries) if e.endswith('Entry')]
        for e in entries:
            self._test_entry_init(vars(v_entries)[e])

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


if __name__ == '__main__':
    import unittest
    unittest.main()