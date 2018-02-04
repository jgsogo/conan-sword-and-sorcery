# -*- coding: utf-8 -*-

import os
import unittest
import platform
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.Executor import Executor
from tests.utils import context_env, TestCaseEnvClean


class TestExecutorAllSettings(TestCaseEnvClean):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_all.py')
        self.n_options = 0
        self.options_multiplier = pow(2, self.n_options)

    def test_linux_gcc(self):
        self.executor = Executor(self.conanfile, osys="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="7"):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 8*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="6,7"):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 16*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="0"):  # Invalid version
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 0 * self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="0,7"):  # Invalid version (fail-safe)
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 0 * self.options_multiplier)

    def test_linux_gcc_and_clang(self):
        self.executor = Executor(self.conanfile, osys="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_CLANG_VERSIONS="5.0"):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 20*self.options_multiplier)

    def test_macos(self):
        self.executor = Executor(self.conanfile, osys="Macos")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0*self.options_multiplier)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="8.1"):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 8*self.options_multiplier)


class TestExecutorAllSettingsAndOptions(TestExecutorAllSettings):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_all_and_options.py')
        self.n_options = 1
        self.options_multiplier = pow(2, self.n_options)


class TestExecutorSettingsNoCompiler(TestCaseEnvClean):
    def setUp(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)

        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_no_compiler.py')
        self.n_options = 1
        self.options_multiplier = pow(2, self.n_options)

    def test_linux(self):
        self.executor = Executor(self.conanfile, osys="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 1 * self.options_multiplier)

    def test_windows(self):
        self.executor = Executor(self.conanfile, osys="Windows")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 1 * self.options_multiplier)

    def test_macos(self):
        self.executor = Executor(self.conanfile, osys="Macos")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 1 * self.options_multiplier)
