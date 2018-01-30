# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan.ci.compiler_registry import CompilerRegistry


class TestCompilerRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = CompilerRegistry()

    def test_base(self):
        self.assertEqual(len(list(self.registry.get_compilers())), 16)
        self.assertEqual(len(list(self.registry.get_compilers(archs=['x86',]))), 8)
        self.assertEqual(len(list(self.registry.get_compilers(archs=['x86',], versions=["7",]))), 2)

    def test_invalid_argument(self):
        self.assertEqual(len(list(self.registry.get_compilers(invalid_arg=["x86", ]))), 0)

    def test_invalid_value(self):
        self.assertEqual(len(list(self.registry.get_compilers(archs=["x86000", ]))), 0)


if __name__ == '__main__':
    unittest.main()
