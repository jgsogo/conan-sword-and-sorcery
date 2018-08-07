# -*- coding: utf-8 -*-

import os
import unittest
import tempfile

from conans.model.settings import Settings
from conans.client.conf import default_settings_yml

from conan_sword_and_sorcery.parsers.settings import get_settings


class TestSettings(unittest.TestCase):

    def test_default_settings(self):
        settings = get_settings()
        self.assertIsInstance(settings, Settings)

    def test_settings_invalid_filename(self):
        with self.assertRaises(IOError):
            get_settings(filename='invalid_filename.txt')

    def test_settings_from_filename(self):
        tf = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tf.write(default_settings_yml)
        tf.close()
        try:
            settings = get_settings(filename=tf.name)
            self.assertIsInstance(settings, Settings)
        finally:
            os.remove(tf.name)
