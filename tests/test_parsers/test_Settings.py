# -*- coding: utf-8 -*-

import os
import unittest

from conans.model.settings import Settings
from conan_sword_and_sorcery.parsers.settings import get_settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings_filename_default = os.path.join(os.path.dirname(__file__), '..', '..', 'conan_sword_and_sorcery', 'conan_settings.yaml')

    def test_default_settings(self):
        settings = get_settings()
        self.assertIsInstance(settings, Settings)

    def test_settings_invalid_filename(self):
        with self.assertRaises(IOError):
            get_settings(filename='invalid_filename.txt')

    def test_settings_filename(self):
        settings = get_settings(filename=self.settings_filename_default)
        self.assertIsInstance(settings, Settings)

