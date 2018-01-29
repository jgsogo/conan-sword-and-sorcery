# -*- coding: utf-8 -*-
import platform
import unittest
from unittest import mock

from conan.ci.settings import Compiler


class TestCompilersWindows(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Windows")

    def test_compilers(self):
        self.assertEqual("Windows", platform.system())
        compilers = Compiler._registry[platform.system()]
        self.assertEqual(len(compilers), 1)
        self.assertEqual(compilers[0].compiler, "Visual Studio")


class TestCompilersLinux(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Linux")

    def test_compilers(self):
        self.assertEqual("Linux", platform.system())
        compilers = Compiler._registry[platform.system()]
        self.assertEqual(len(compilers), 2)
        self.assertEqual(compilers[0].compiler, "gcc")
        self.assertEqual(compilers[1].compiler, "clang")


class TestCompilersDarwin(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Darwin")

    def test_compilers(self):
        self.assertEqual("Darwin", platform.system())
        compilers = Compiler._registry[platform.system()]
        self.assertEqual(len(compilers), 1)
        self.assertEqual(compilers[0].compiler, "apple-clang")

