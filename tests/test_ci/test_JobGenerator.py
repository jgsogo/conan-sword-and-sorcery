# -*- coding: utf-8 -*-

import os
import unittest
import platform
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.job_generator import JobGenerator, print_jobs
from tests.utils import context_env, TestCaseEnvClean


class TestExecutorAllSettings(TestCaseEnvClean):

    @property
    def options_multiplier(self):
        if len(self.options):
            return pow(2, len(self.options.split(',')))
        return 1

    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_all.py')
        self.options = ''

    def test_linux_gcc(self):
        self.executor = JobGenerator(self.conanfile, osys="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_OPTIONS=self.options):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 8*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="6,7", CONAN_OPTIONS=self.options):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 16*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="0", CONAN_OPTIONS=self.options):  # Invalid version
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 0 * self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="0,7", CONAN_OPTIONS=self.options):  # Invalid version (fail-safe)
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 0 * self.options_multiplier)

    def test_linux_gcc_and_clang(self):
        self.executor = JobGenerator(self.conanfile, osys="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_CLANG_VERSIONS="5.0", CONAN_OPTIONS=self.options):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 20*self.options_multiplier)

    def test_macos(self):
        self.executor = JobGenerator(self.conanfile, osys="Darwin")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0*self.options_multiplier)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="8.1", CONAN_OPTIONS=self.options):
            jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(jobs), 8*self.options_multiplier)


class TestExecutorAllSettingsAndOptions(TestExecutorAllSettings):

    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_all_and_options.py')
        self.options = 'shared'


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
        with context_env(CONAN_OPTIONS='shared'):
            self.executor = JobGenerator(self.conanfile, osys="Linux")
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 1 * self.options_multiplier)

    def test_windows(self):
        with context_env(CONAN_OPTIONS='shared'):
            self.executor = JobGenerator(self.conanfile, osys="Windows")
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 1 * self.options_multiplier)

    def test_macos(self):
        with context_env(CONAN_OPTIONS='shared'):
            self.executor = JobGenerator(self.conanfile, osys="Darwin")
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 1 * self.options_multiplier)
