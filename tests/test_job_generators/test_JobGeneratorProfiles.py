# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
try:
    from unittest import mock
except ImportError:
    import mock

from conans.errors import ConanException

from conan_sword_and_sorcery.parsers.profile import profile_for
from conan_sword_and_sorcery.job_generators.profiles_generator import JobGeneratorProfiles
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.parsers.conanfile import ConanFileWrapper
from conan_sword_and_sorcery.ci.compilers.clang import CompilerClangApple, CompilerClangLinux
from conan_sword_and_sorcery.utils import platform_system

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
        tmp_dir = tempfile.mkdtemp()
        try:
            # Generate a couple of random profiles
            profiles_dir = os.path.join(tmp_dir, '.conan', 'profiles')
            os.makedirs(profiles_dir)
            with profile_for(CompilerClangApple(arch='x86', build_type='Release', version='7.3', libcxx='libc++'), basepath=profiles_dir) as _1:
                with profile_for(CompilerClangLinux(arch='x86', build_type='Release', version='4.0', libcxx='libstdc++'), basepath=profiles_dir) as _2:
                    with context_env(CONAN_USER_HOME=tmp_dir):
                        generator = JobGeneratorProfiles(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys=platform_system())
                        self.assertEqual(len(list(generator.enumerate_jobs())), 2)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_empty_profile_list(self):
        generator = JobGeneratorProfiles(conanfile_wrapper=self.conanfile_wrapper, settings=self.settings, osys=platform_system())
        with context_env(CONAN_USER_HOME='non-existing-path'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 0)

