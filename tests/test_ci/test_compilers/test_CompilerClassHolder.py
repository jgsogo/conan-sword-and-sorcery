# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.compilers.registry import CompilerClassHolder
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


class TestCompiler(BaseCompiler):
    id = 'test_compiler'
    osys = 'test_os'

    @classmethod
    def validate(self, param3=None, **kwargs):
        return param3 != 'invalid'


class TestCompilerClassHolder(unittest.TestCase):

    def setUp(self):
        self.param1_values = ["a", "b", "c", ]
        self.param2_values = ["1", "2"]
        self.param3_values = ["invalid", "valid", ]
        self.holder = CompilerClassHolder(TestCompiler, param1=self.param1_values, param2=self.param2_values, param3=self.param3_values)

    def test_base(self):
        self.assertListEqual(self.holder.get_configurations(key='param1'), self.param1_values)
        self.assertListEqual(self.holder.get_configurations(key='param2'), self.param2_values)

    def test_explode(self):
        explosion = list(self.holder.explode())
        self.assertEqual(len(explosion), len(self.param1_values)*len(self.param2_values))
        for it in explosion:
            self.assertTrue(isinstance(it, TestCompiler))

    def test_explode_filtered(self):
        my_param1_values = ["a", "b"]
        explosion = list(self.holder.explode(param1=my_param1_values))
        self.assertEqual(len(explosion), len(my_param1_values) * len(self.param2_values))

    def test_explode_filter_invalid(self):
        my_param1_values = ["d", ]
        with self.assertRaises(ValueError):
            list(self.holder.explode(param1=my_param1_values))

        with self.assertRaises(ValueError):
            list(self.holder.explode(param23=[1, 2]))


if __name__ == '__main__':
    unittest.main()
