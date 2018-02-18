# -*- coding: utf-8 -*-

import unittest
import os

from conan_sword_and_sorcery.ci.settings import Settings, ConanSettings
from conan_sword_and_sorcery.ci.compilers import CompilerRegistry


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings_filename_default = os.path.join(os.path.dirname(__file__), '..', '..', 'conan_sword_and_sorcery', 'conan_settings.yaml')

    def test_default_settings(self):
        settings = Settings.default()
        self.assertIsInstance(settings, ConanSettings)

        settings2 = Settings()
        self.assertEqual(settings.values_list, settings2.conan_settings.values_list)

    def test_settings_invalid_filename(self):
        with self.assertRaises(IOError):
            Settings(settings_filename='invalid_filename.txt')

    def test_settings_filename(self):
        settings = Settings(settings_filename=self.settings_filename_default)
        self.assertIsInstance(settings.conan_settings, ConanSettings)

