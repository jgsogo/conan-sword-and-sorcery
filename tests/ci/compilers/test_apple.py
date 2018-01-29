# -*- coding: utf-8 -*-

import platform
import unittest
from unittest import mock

from conan.ci.compilers import CompilerClangApple
from conan.ci.settings import Compiler, get_settings
from tests.utils import context_env


class TestCompilersWindows(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Darwin")
        self.n_versions = len(CompilerClangApple().version)
        self.n_build_types = len(CompilerClangApple().build_type)
        self.n_archs = len(CompilerClangApple().arch)

    def test_default(self):
        compilers = Compiler._registry[platform.system()]
        vs = compilers[0]
        self.assertEqual(vs, CompilerClangApple)
        self.assertEqual(vs.compiler, "apple-clang")
        self.assertEqual(vs.os_system, "Darwin")

        configurations = get_settings()
        self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions*self.n_build_types)

    def test_versions(self):
        with context_env(CONAN_APPLE_CLANG_VERSIONS='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*1*self.n_build_types)

        with context_env(CONAN_APPLE_CLANG_VERSIONS='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*2*self.n_build_types)

    def test_build_types(self):
        with context_env(CONAN_BUILD_TYPES='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions * 1)

        with context_env(CONAN_BUILD_TYPES='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions * 2)


if __name__ == '__main__':
    unittest.main()
