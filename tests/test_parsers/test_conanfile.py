# -*- coding: utf-8 -*-

import os
import unittest

from conan_sword_and_sorcery.parsers.conanfile import ConanfileWrapper


class TestParserConanfile01(unittest.TestCase):

    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        conanfile01 = os.path.join(single_files, 'conanfile01.py')
        self.wrapper = ConanfileWrapper.parse(conanfile01)

    def test_basic(self):
        self.assertEqual(self.wrapper.name, "gtest")
        self.assertEqual(self.wrapper.version, "1.8.0")

    def test_options(self):
        options = self.wrapper.options
        self.assertSetEqual(set(options.keys()), {'shared', 'build_gmock', 'fpic'})

    def test_conjugations(self):
        self.assertEqual(len(list(self.wrapper.conjugate_options(['shared', 'build_gmock', 'fpic', ]))), 2*2*2)
        self.assertEqual(len(list(self.wrapper.conjugate_options(['shared', 'build_gmock', ]))), 2 * 2)
        self.assertEqual(len(list(self.wrapper.conjugate_options(['shared', ]))), 2)
        self.assertEqual(self.wrapper.conjugate_options([]), None)


if __name__ == '__main__':
    unittest.main()
