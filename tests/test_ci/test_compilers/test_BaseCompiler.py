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



if __name__ == '__main__':
    unittest.main()
