# -*- coding: utf-8 -*-

import platform
import unittest
from unittest import mock

from conan.ci.compilers import CompilerVisualStudio
from conan.ci.settings import Compiler, get_settings
from tests.utils import context_env


class TestCompilerVisualStudio(unittest.TestCase):
    def setUp(self):
        platform.system = mock.Mock(return_value="Windows")
        self.n_versions = len(CompilerVisualStudio().version)
        self.n_runtimes = len(CompilerVisualStudio().runtime)
        self.n_build_types = len(CompilerVisualStudio().build_type)
        self.n_archs = len(CompilerVisualStudio().arch)

    def test_default(self):
        compilers = Compiler._registry[platform.system()]
        vs = compilers[0]
        self.assertEqual(vs, CompilerVisualStudio)
        self.assertEqual(vs.compiler, "Visual Studio")
        self.assertEqual(vs.os_system, "Windows")

        configurations = get_settings()
        self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions*self.n_runtimes*self.n_build_types)

    def test_versions(self):
        with context_env(CONAN_VISUAL_VERSIONS='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*1*self.n_runtimes*self.n_build_types)

        with context_env(CONAN_VISUAL_VERSIONS='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*2*self.n_runtimes*self.n_build_types)

    def test_runtimes(self):
        with context_env(CONAN_VISUAL_RUNTIMES='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions * 1 * self.n_build_types)

        with context_env(CONAN_VISUAL_RUNTIMES='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions * 2 * self.n_build_types)

    def test_build_types(self):
        with context_env(CONAN_BUILD_TYPES='22'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions * self.n_runtimes * 1)

        with context_env(CONAN_BUILD_TYPES='22,33'):
            configurations = get_settings()
            self.assertEqual(len(list(configurations)), self.n_archs*self.n_versions * self.n_runtimes * 2)


if __name__ == '__main__':
    unittest.main()