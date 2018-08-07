# -*- coding: utf-8 -*-

import os
try:
    from unittest import mock
except ImportError:
    import mock

from conans.errors import ConanException

from conan_sword_and_sorcery.job_generators.profiles_generator import JobGeneratorProfiles
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

    def test_default_profile_list(self):
        generator = JobGeneratorProfiles(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Linux")
        self.assertTrue(len(list(generator.enumerate_jobs())) != 0)

    def test_empty_profile_list(self):
        generator = JobGeneratorProfiles(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys="Linux")
        with context_env(CONAN_USER_HOME='non-existing-path'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 0)

