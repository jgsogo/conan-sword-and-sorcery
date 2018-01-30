# -*- coding: utf-8 -*-

import unittest
import platform
try:
    from unittest import mock
except ImportError:
    import mock
from collections import defaultdict

from conan.ci.compilers import Compiler, get_compilers, get_available_configurations, register
from conan.utils import isstr


@register
class TestCompiler01(Compiler):
    compiler = '01'
    os_system = "TestPlatform"

    @property
    def version(self):
        return ["01_v1", "01_v2", ]


@register
class TestCompiler02(Compiler):
    compiler = '02'
    os_system = "TestPlatform"
    _configurations = Compiler._configurations + ["test_config"]

    @property
    def version(self):
        return ["02_v1", "02_v2", ]

    @property
    def test_config(self):
        return ["1", "2", "3",]


class TestGetSettingsFunction(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="TestPlatform")
        self.configurations = get_available_configurations()
        self.n_build_types = len(Compiler().build_type)
        self.n_archs = len(Compiler().arch)

    def test_total(self):
        n_total = sum(len(configs) for c, configs in self.configurations)
        self.assertEqual(n_total, self.n_archs*16)

    def test_compiler01(self):
        confs = list(filter(lambda x: x[0].compiler == TestCompiler01.compiler, self.configurations))
        self.assertEqual(len(confs), 1)

        compiler, configs = confs[0]
        self.assertTrue(isinstance(compiler, TestCompiler01))
        self.assertEqual(len(configs), self.n_archs * self.n_build_types * len(TestCompiler01().version))

        all_config_options = defaultdict(set)
        for pack in configs:
            for key, val in pack.items():
                all_config_options[key].add(val)

        # TestCompiler01 does not define 'test_config'
        self.assertListEqual(sorted(list(all_config_options.keys())), sorted(['build_type', 'arch', 'version']))

    def test_compiler02(self):
        confs = list(filter(lambda x: x[0].compiler == TestCompiler02.compiler, self.configurations))
        self.assertEqual(len(confs), 1)

        compiler, configs = confs[0]
        self.assertTrue(isinstance(compiler, TestCompiler02))
        self.assertEqual(len(configs), self.n_archs * self.n_build_types * len(TestCompiler02().version) * len(TestCompiler02().test_config))

        all_config_options = defaultdict(set)
        for pack in configs:
            for key, val in pack.items():
                all_config_options[key].add(val)

        # TestCompiler01 does not define 'test_config'
        self.assertListEqual(sorted(list(all_config_options.keys())), sorted(['build_type', 'arch', 'version', 'test_config']))
