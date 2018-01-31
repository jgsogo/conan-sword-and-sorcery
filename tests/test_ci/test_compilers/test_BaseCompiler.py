# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan.ci.compilers.base_compiler import BaseCompiler


class TestBaseCompiler(unittest.TestCase):

    def test_invalid_constructor(self):
        with self.assertRaises(ValueError):
            compiler = BaseCompiler(name='testing', tt=[])

    def test_max_configurations(self):
        compiler = BaseCompiler(name='testing', archs=["1", "2", ], rrs=["a", "b", "c", ])
        self.assertEqual(compiler.max_configurations(), 2*3)


if __name__ == '__main__':
    unittest.main()
