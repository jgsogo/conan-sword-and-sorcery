# -*- coding: utf-8 -*-
import unittest

from conan_sword_and_sorcery.utils import slice


class TestSlice(unittest.TestCase):

    def test_corner_cases(self):
        with self.assertRaises(AssertionError):
            slice(13, 0, 1)
        with self.assertRaises(AssertionError):
            slice(13, 2, 1)
        with self.assertRaises(AssertionError):
            slice(13, 0, 0)
        with self.assertRaises(AssertionError):
            slice(13, 1, 0)
        with self.assertRaises(AssertionError):
            slice(0, 1, 2)
        with self.assertRaises(AssertionError):
            slice(10, 1, 12)

    def test_slice_basic(self):
        self.assertEqual(slice(13, 1, 5), (0, 3))
        self.assertEqual(slice(13, 2, 5), (3, 6))
        self.assertEqual(slice(13, 3, 5), (6, 9))
        self.assertEqual(slice(13, 4, 5), (9, 11))
        self.assertEqual(slice(13, 5, 5), (11, 13))

    def test_slice_items(self):
        total = 13
        ll = [x for x in range(total)]

        init, end = slice(total, 1, 5)
        self.assertListEqual(ll[init:end], [0, 1, 2])

        init, end = slice(total, 2, 5)
        self.assertListEqual(ll[init:end], [3, 4, 5])

        init, end = slice(total, 3, 5)
        self.assertListEqual(ll[init:end], [6, 7, 8])

        init, end = slice(total, 4, 5)
        self.assertListEqual(ll[init:end], [9, 10])

        init, end = slice(total, 5, 5)
        self.assertListEqual(ll[init:end], [11, 12])
