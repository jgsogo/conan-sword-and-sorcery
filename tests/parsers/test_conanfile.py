# -*- coding: utf-8 -*-

import os
import unittest

from conan.parsers.conanfile import ConanfileWrapper


class TestParserConanfile01(unittest.TestCase):

    def setUp(self):
        import logging
        logging.basicConfig()
        logger = logging.getLogger('conan')
        logger.setLevel(logging.DEBUG)

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

    def test_configurations(self):
        self.assertEqual(len(list(self.wrapper.get_configurations())), 2*2*2)


if __name__ == '__main__':
    unittest.main()
