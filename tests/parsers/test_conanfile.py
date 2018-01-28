# -*- coding: utf-8 -*-

import os
import unittest

from conan.parsers.conanfile import ConanfileParser


class TestParser(unittest.TestCase):

    def setUp(self):
        import logging
        logging.basicConfig()
        logger = logging.getLogger('conan')
        logger.setLevel(logging.DEBUG)

        me = os.path.dirname(__file__)
        self.single_files = os.path.join(me, '..', 'files', 'single')

    def test_conanfile01(self):
        conanfile01 = os.path.join(self.single_files, 'conanfile01.py')
        recipe = ConanfileParser.parse(conanfile01)
        self.assertEqual(recipe.name, "gtest")
        self.assertEqual(recipe.version, "1.8.0")
        print(recipe.options)

if __name__ == '__main__':
    unittest.main()
