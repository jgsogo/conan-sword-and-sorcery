# -*- coding: utf-8 -*-

import platform
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan.ci.compilers import Compiler, CompilerClangApple, get_available_configurations, get_compilers
from tests.utils import context_env


class TestCompilersApple(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Darwin")
        self.n_versions = len(CompilerClangApple().version)
        self.n_build_types = len(CompilerClangApple().build_type)
        self.n_archs = len(CompilerClangApple().arch)

    def test_default(self):
        compilers = get_compilers(platform.system())
        apple_clang = compilers[0]
        self.assertEqual(apple_clang, CompilerClangApple)
        self.assertEqual(apple_clang.compiler, "apple-clang")
        self.assertEqual(apple_clang.os_system, "Darwin")

        configurations = get_available_configurations(compilers)
        apple_clang_compiler, apple_clang_configurations = configurations[0]
        self.assertEqual(len(list(apple_clang_configurations)), self.n_archs*self.n_versions*self.n_build_types)

    def test_versions(self):
        with context_env(CONAN_APPLE_CLANG_VERSIONS='22'):
            configurations = get_available_configurations()
            apple_clang_compiler, apple_clang_configurations = configurations[0]
            self.assertEqual(len(list(apple_clang_configurations)), self.n_archs*1*self.n_build_types)

        with context_env(CONAN_APPLE_CLANG_VERSIONS='22,33'):
            configurations = get_available_configurations()
            apple_clang_compiler, apple_clang_configurations = configurations[0]
            self.assertEqual(len(list(apple_clang_configurations)), self.n_archs*2*self.n_build_types)

    def test_build_types(self):
        with context_env(CONAN_BUILD_TYPES='22'):
            configurations = get_available_configurations()
            apple_clang_compiler, apple_clang_configurations = configurations[0]
            self.assertEqual(len(list(apple_clang_configurations)), self.n_archs*self.n_versions * 1)

        with context_env(CONAN_BUILD_TYPES='22,33'):
            configurations = get_available_configurations()
            apple_clang_compiler, apple_clang_configurations = configurations[0]
            self.assertEqual(len(list(apple_clang_configurations)), self.n_archs*self.n_versions * 2)


if __name__ == '__main__':
    unittest.main()
