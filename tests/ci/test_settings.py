# -*- coding: utf-8 -*-

import unittest
import platform
from unittest import mock
from collections import defaultdict

from conan.ci.compilers import Compiler
from conan.ci.settings import get_settings
from conan.utils import isstr


@Compiler.register
class TestCompiler01(Compiler):
    compiler = '01'
    os_system = "TestPlatform"

    @property
    def version(self):
        return ["01_v1", "01_v2", ]


@Compiler.register
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
        self.configurations = list(get_settings())
        self.n_build_types = len(Compiler().build_type)
        self.n_archs = len(Compiler().arch)

    def test_total(self):
        self.assertEqual(len(self.configurations), self.n_archs*16)

    def test_compiler01(self):
        confs = list(filter(lambda x: isinstance(x[1], TestCompiler01), self.configurations))
        self.assertEqual(len(confs), self.n_archs * self.n_build_types * len(TestCompiler01().version))

        all_config_options = defaultdict(set)
        for os_system, compiler, config in confs:
            self.assertEqual(os_system, "TestPlatform")
            self.assertTrue(isinstance(compiler, TestCompiler01))
            for key, value in config.items():
                all_config_options[key].add(value)

        # All options must be seen
        for item in TestCompiler01._configurations:
            value = getattr(TestCompiler01(), item)
            self.assertSetEqual(set(value) if not isstr(value) else set([value,]), all_config_options[item])

        # TestCompiler01 does not define 'test_config'
        self.assertSetEqual(all_config_options["test_config"], {None, })

    def test_compiler02(self):
        confs = list(filter(lambda x: isinstance(x[1], TestCompiler02), self.configurations))
        self.assertEqual(len(confs), self.n_archs*self.n_build_types * len(TestCompiler02().version) * len(TestCompiler02().test_config))

        all_config_options = defaultdict(set)
        for os_system, compiler, config in confs:
            self.assertEqual(os_system, "TestPlatform")
            self.assertTrue(isinstance(compiler, TestCompiler02))
            for key, value in config.items():
                all_config_options[key].add(value)

        # All options must be seen
        for item in TestCompiler02._configurations:
            value = getattr(TestCompiler02(), item)
            self.assertSetEqual(set(value) if not isstr(value) else set([value,]), all_config_options[item])
