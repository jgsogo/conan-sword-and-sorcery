# -*- coding: utf-8 -*-

import platform
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan.ci.compilers import CompilerGCC, CompilerClangLinux, Compiler, get_compilers, get_available_configurations
from tests.utils import context_env


class TestCompilersLinux(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Linux")
        self.n_gcc_versions = len(CompilerGCC().version)
        self.n_gcc_build_types = len(CompilerGCC().build_type)
        self.n_clang_versions = len(CompilerClangLinux().version)
        self.n_clang_build_types = len(CompilerClangLinux().build_type)
        self.n_archs = len(CompilerClangLinux().arch)

    def test_default(self):
        compilers = get_compilers(platform.system())

        # GCC
        gcc = compilers[0]
        self.assertEqual(gcc, CompilerGCC)
        self.assertEqual(gcc.compiler, "gcc")
        self.assertEqual(gcc.os_system, "Linux")

        # Clang
        clang = compilers[1]
        self.assertEqual(clang, CompilerClangLinux)
        self.assertEqual(clang.compiler, "clang")
        self.assertEqual(clang.os_system, "Linux")

        configurations = get_available_configurations()
        n_total = sum(len(configs) for c, configs in configurations)
        self.assertEqual(n_total,
                         self.n_archs*(
                             self.n_gcc_versions*self.n_gcc_build_types +
                             self.n_clang_versions*self.n_clang_build_types))

    def test_versions(self):
        with context_env(CONAN_GCC_VERSIONS='1'):
            configurations = get_available_configurations()
            n_total = sum(len(configs) for c, configs in configurations)
            self.assertEqual(n_total, self.n_archs*(1*self.n_gcc_build_types + self.n_clang_versions*self.n_clang_build_types))

        with context_env(CONAN_GCC_VERSIONS='1', CONAN_CLANG_VERSIONS='2'):
            configurations = get_available_configurations()
            n_total = sum(len(configs) for c, configs in configurations)
            self.assertEqual(n_total, self.n_archs*(1*self.n_gcc_build_types + 1*self.n_clang_build_types))

        with context_env(CONAN_GCC_VERSIONS='1,2', CONAN_CLANG_VERSIONS='2'):
            configurations = get_available_configurations()
            n_total = sum(len(configs) for c, configs in configurations)
            self.assertEqual(n_total, self.n_archs*(2*self.n_gcc_build_types + 1*self.n_clang_build_types))

    def test_build_types(self):
        with context_env(CONAN_BUILD_TYPES='22'):
            configurations = get_available_configurations()
            n_total = sum(len(configs) for c, configs in configurations)
            self.assertEqual(n_total, self.n_archs*(self.n_gcc_versions * 1 + self.n_clang_versions * 1))

        with context_env(CONAN_BUILD_TYPES='22,33'):
            configurations = get_available_configurations()
            n_total = sum(len(configs) for c, configs in configurations)
            self.assertEqual(n_total, self.n_archs*(self.n_gcc_versions*2 + self.n_clang_versions*2))


if __name__ == '__main__':
    unittest.main()
