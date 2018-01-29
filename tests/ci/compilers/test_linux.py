# -*- coding: utf-8 -*-

import platform
import unittest
from unittest import mock

from conan.ci.compilers import CompilerGCC, CompilerClangLinux, Compiler
from conan.ci.settings import get_settings
from tests.utils import context_env


class TestCompilersLinux(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Linux")
        self.n_gcc_versions = len(CompilerGCC().versions)
        self.n_gcc_build_types = len(CompilerGCC().build_types)
        self.n_clang_versions = len(CompilerClangLinux().versions)
        self.n_clang_build_types = len(CompilerClangLinux().build_types)

    def test_default(self):
        compilers = Compiler._registry[platform.system()]

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

        configurations = get_settings()
        self.assertEqual(len(list(configurations)),
                         self.n_gcc_versions*self.n_gcc_build_types +
                         self.n_clang_versions*self.n_clang_build_types)

    def test_versions(self):
        with context_env(CONAN_GCC_VERSIONS='1'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)),
                             1*self.n_gcc_build_types +
                             self.n_clang_versions * self.n_clang_build_types)

        with context_env(CONAN_GCC_VERSIONS='1', CONAN_CLANG_VERSIONS='2'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)),
                             1*self.n_gcc_build_types +
                             1*self.n_clang_build_types)

        with context_env(CONAN_VISUAL_VERSIONS='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), 2*self.n_runtimes*self.n_build_types)

    def test_runtimes(self):
        with context_env(CONAN_VISUAL_RUNTIMES='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_versions * 1 * self.n_build_types)

        with context_env(CONAN_VISUAL_RUNTIMES='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_versions * 2 * self.n_build_types)

    def test_build_types(self):
        with context_env(CONAN_BUILD_TYPES='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_versions * self.n_runtimes * 1)

        with context_env(CONAN_BUILD_TYPES='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_versions * self.n_runtimes * 2)


if __name__ == '__main__':
    unittest.main()
