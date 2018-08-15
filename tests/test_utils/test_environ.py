# -*- coding: utf-8 -*-
import os
import unittest
import re

from conan_sword_and_sorcery.utils.environ import context_env, clean_context_env


class TestContextEnv(unittest.TestCase):

    def test_new_variable(self):
        with context_env(MYVAR="value"):
            self.assertIn("MYVAR", os.environ)
            self.assertEqual(os.environ['MYVAR'], "value")
        self.assertNotIn("MYVAR", os.environ)

    def test_existing_variable(self):
        key1 = list(os.environ.keys())[0]
        value1 = os.environ[key1]
        value_for_testing = "new-value-for-testing"
        self.assertNotEqual(value1, value_for_testing)
        with context_env(**{key1: value_for_testing}):
            print(os.environ[key1])
            self.assertIn(key1, os.environ)
            self.assertEqual(os.environ[key1], value_for_testing)
        self.assertEqual(os.environ[key1], value1)


class TestCleanContextEnv(unittest.TestCase):
    def test_conan_pattern(self):
        with context_env(CONAN_VAR1="value", CONAN_VAR2="value2"):
            self.assertIn("CONAN_VAR1", os.environ.keys())
            self.assertIn("CONAN_VAR2", os.environ.keys())
            with clean_context_env(pattern=r'CONAN_.*'):
                self.assertNotIn("CONAN_VAR1", os.environ.keys())
                self.assertNotIn("CONAN_VAR2", os.environ.keys())
            self.assertIn("CONAN_VAR1", os.environ.keys())
            self.assertEqual(os.environ["CONAN_VAR1"], "value")
            self.assertIn("CONAN_VAR2", os.environ.keys())
            self.assertEqual(os.environ["CONAN_VAR2"], "value2")

    def test_multi_pattern(self):
        with context_env(CONAN_VAR1="value", APPVEYOR_VAR2="value2", APPVEYOR_VAR="other"):
            pattern = r'^(CONAN_.*)|(^APPVEYOR_[A-Z]+)$'
            self.assertFalse(re.match(pattern, "APPVEYOR_VAR2"))
            with clean_context_env(pattern=pattern):
                self.assertNotIn("CONAN_VAR1", os.environ.keys())
                self.assertNotIn("APPVEYOR_VAR", os.environ.keys())
                self.assertIn("APPVEYOR_VAR2", os.environ.keys())

