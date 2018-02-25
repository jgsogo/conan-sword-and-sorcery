# -*- coding: utf-8 -*-

import os
import unittest

from conans.model.settings import Settings
from conan_sword_and_sorcery.parsers.settings import get_settings


class TestSettings(unittest.TestCase):

    def test_default_settings(self):
        settings = get_settings()
        self.assertIsInstance(settings, Settings)

    def test_settings_invalid_filename(self):
        with self.assertRaises(IOError):
            get_settings(filename='invalid_filename.txt')


