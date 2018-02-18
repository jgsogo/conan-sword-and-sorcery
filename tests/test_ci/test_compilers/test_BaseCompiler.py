# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


class ATestCompiler(BaseCompiler):
    id = 'test_compiler'
    osys = 'test_os'


class TestBaseCompiler(unittest.TestCase):

    def test_invalid_constructor(self):
        with self.assertRaises(ValueError):
            ATestCompiler(tt=[])
        with self.assertRaises(ValueError):
            ATestCompiler(anything=None)
        with self.assertRaises(ValueError):
            ATestCompiler(anything=23)

    def test_getattr(self):
        a = ATestCompiler(attr="attr")
        self.assertEqual(a.id, ATestCompiler.id)
        self.assertEqual(a.os, ATestCompiler.osys)
        self.assertEqual(a.attr, "attr")

    def test_environment_filters(self):
        with self.assertRaises(NotImplementedError):
            ATestCompiler.environment_filters()


if __name__ == '__main__':
    unittest.main()
