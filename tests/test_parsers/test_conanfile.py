# -*- coding: utf-8 -*-

import os
import unittest

from conan_sword_and_sorcery.parsers.conanfile import ConanFileWrapper
from conan_sword_and_sorcery.parsers.settings import get_settings


class TestParserConanfile01(unittest.TestCase):

    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile01 = os.path.join(single_files, 'conanfile01.py')
        self.wrapper = ConanFileWrapper.parse(self.conanfile01)
        self.wrapper.instantiate(settings=get_settings())

    def test_not_valid_filename(self):
        with self.assertRaises(Exception):
            ConanFileWrapper.parse("<invalid-filename>")
        with self.assertRaises(Exception):
            ConanFileWrapper.parse(os.path.abspath(__file__))

    def test_not_instantiated(self):
        wrapper = ConanFileWrapper.parse(self.conanfile01)
        with self.assertRaisesRegexp(RuntimeError, "Instantiate recipe first"):
            wrapper.settings_keys()
        with self.assertRaisesRegexp(RuntimeError, "Instantiate recipe first"):
            wrapper.options_keys()
        with self.assertRaisesRegexp(RuntimeError, "Instantiate recipe first"):
            _ = wrapper.name

    def test_basic(self):
        self.assertEqual(self.wrapper.name, "gtest")
        self.assertEqual(self.wrapper.version, "1.8.0")

    def test_options(self):
        self.assertSetEqual(set(self.wrapper.options_keys()), {'shared', 'build_gmock', 'fpic'})

    def test_conjugations(self):
        self.assertEqual(len(list(self.wrapper.conjugate_options(['shared', 'build_gmock', 'fpic', ]))), 2*2*2)
        self.assertEqual(len(list(self.wrapper.conjugate_options(['shared', 'build_gmock', ]))), 2 * 2)
        self.assertEqual(len(list(self.wrapper.conjugate_options(['shared', ]))), 2)
        self.assertEqual(self.wrapper.conjugate_options([]), None)


if __name__ == '__main__':
    unittest.main()
