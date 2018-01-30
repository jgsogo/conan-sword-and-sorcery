# -*- coding: utf-8 -*-
import platform
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan.ci.compilers import Compiler, get_compilers


class TestCompilersWindows(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Windows")

    def test_compilers(self):
        self.assertEqual("Windows", platform.system())
        compilers = get_compilers(platform.system())
        self.assertEqual(len(compilers), 1)
        self.assertEqual(compilers[0].compiler, "Visual Studio")


class TestCompilersLinux(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Linux")

    def test_compilers(self):
        self.assertEqual("Linux", platform.system())
        compilers = get_compilers(platform.system())
        self.assertEqual(len(compilers), 2)
        self.assertEqual(compilers[0].compiler, "gcc")
        self.assertEqual(compilers[1].compiler, "clang")


class TestCompilersDarwin(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Darwin")

    def test_compilers(self):
        self.assertEqual("Darwin", platform.system())
        compilers = get_compilers(platform.system())
        self.assertEqual(len(compilers), 1)
        self.assertEqual(compilers[0].compiler, "apple-clang")

