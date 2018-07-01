# -*- coding: utf-8 -*-

import os
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.job_generators.environ_generator import JobGeneratorEnviron
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.parsers.conanfile import ConanFileWrapper

from tests.utils import TestCaseEnvClean
from conan_sword_and_sorcery.utils.environ import context_env


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
        self.conanfile_wrapper = ConanFileWrapper.parse(self.conanfile)
        self.settings = get_settings()
        self.options = ''

    def test_linux_gcc(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Linux")

        with context_env(CONAN_OPTIONS=self.options):
            self.assertEqual(len(list(generator.enumerate_jobs())), 68*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_OPTIONS=self.options):
            jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(jobs), 8*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="6,7", CONAN_OPTIONS=self.options):
            jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(jobs), 16*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="0", CONAN_OPTIONS=self.options):  # Invalid version
            jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(jobs), 0 * self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="0,7", CONAN_OPTIONS=self.options):  # Invalid version (fail-safe)
            jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(jobs), 8 * self.options_multiplier)

    def test_linux_gcc_and_clang(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Linux")

        with context_env(CONAN_OPTIONS=self.options):
            self.assertEqual(len(list(generator.enumerate_jobs())), 68*self.options_multiplier)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_CLANG_VERSIONS="5.0", CONAN_OPTIONS=self.options):
            jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(jobs), 20*self.options_multiplier)

    def test_macos(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Macos")

        with context_env(CONAN_OPTIONS=self.options):
            self.assertEqual(len(list(generator.enumerate_jobs())), 32*self.options_multiplier)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="8.1", CONAN_OPTIONS=self.options):
            jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(jobs), 8*self.options_multiplier)


class TestExecutorAllSettingsAndOptions(TestExecutorAllSettings):

    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_all_and_options.py')
        self.conanfile_wrapper = ConanFileWrapper.parse(self.conanfile)
        self.settings = get_settings()
        self.options = 'shared'


class TestExecutorSettingsNoCompiler(TestCaseEnvClean):
    def setUp(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)

        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'settings_no_compiler.py')
        self.conanfile_wrapper = ConanFileWrapper.parse(self.conanfile)
        self.settings = get_settings()
        self.n_options = 1
        self.options_multiplier = pow(2, self.n_options)

    def test_linux(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Linux")
        with context_env(CONAN_OPTIONS='shared'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1 * self.options_multiplier)

    def test_windows(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Windows")
        with context_env(CONAN_OPTIONS='shared'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1 * self.options_multiplier)

    def test_macos(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Macos")
        with context_env(CONAN_OPTIONS='shared'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1 * self.options_multiplier)
