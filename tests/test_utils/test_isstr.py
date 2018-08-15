# -*- coding: utf-8 -*-

import unittest

from conan_sword_and_sorcery.utils import isstr


class TestIsStr(unittest.TestCase):

    def test_true(self):
        self.assertTrue(isstr("string"))
        self.assertTrue(isstr(u"string"))
        self.assertTrue(isstr(str(23)))
        self.assertTrue(isstr(b"string"))

    def test_false(self):
        self.assertFalse(isstr(23))
        self.assertFalse(isstr(False))
        self.assertFalse(isstr(["a"]))
        self.assertFalse(isstr(["a", "b", ]))
