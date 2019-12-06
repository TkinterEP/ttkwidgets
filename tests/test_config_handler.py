# Copyright (c) RedFantom 2017
# For license see LICENSE
from ttkwidgets import Config
from tests import BaseWidgetTest
import tkinter as tk
import pathlib


class TestConfig(BaseWidgetTest):
    def test_singleton(self):
        config_1 = Config('tests/testfiles/test.json')
        config_2 = Config('tests/testfiles/test.json')
        self.assertIs(config_1, config_2)

    def test_loading(self):
        config = Config('tests/testfiles/test.json')
        config.load()

    def test_saving(self):
        config = Config('tests/testfiles/test.json')
        config.load()
        config.path = 'tests/testfiles/test_save.json'
        config.save()
    
    def test_path_setting(self):
        config = Config('tests/testfiles/test.json')
        self.assertIsInstance(config.path, pathlib.Path)
        with self.assertRaises(TypeError):
            config.path = 1

    def test_config_variable_type(self):
        config = Config('tests/testfiles/test.json')
        config.load()
        self.assertIsInstance(config['integer'], tk.IntVar)
        self.assertIsInstance(config['floating_point'], tk.DoubleVar)
        self.assertIsInstance(config['string'], tk.StringVar)
        self.assertIsInstance(config['boolean'], tk.IntVar)

    def test_config_variable_value(self):
        config = Config('tests/testfiles/test.json')
        config.load()
        self.assertEquals(config['integer'].get(), 1)
        self.assertEquals(config['floating_point'].get(), 2.5)
        self.assertEquals(config['string'].get(), 'string')
        self.assertEquals(config['boolean'].get(), True)
