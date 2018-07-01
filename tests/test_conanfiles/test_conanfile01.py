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


class TestConanfile01(TestCaseEnvClean):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        conanfile01 = os.path.join(single_files, 'conanfile01.py')
        self.wrapper = ConanFileWrapper.parse(conanfile01)
        self.settings = get_settings()

    def test_total_macos(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Macos")
        self.assertEqual(len(list(generator.enumerate_jobs())), 32)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="7.3"):
            self.assertEqual(len(list(generator.enumerate_jobs())), 8)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="7.3", CONAN_BUILD_TYPES="Release", CONAN_ARCHS="x86_64"):
            self.assertEqual(len(list(generator.enumerate_jobs())), 2)

    def test_total_linux(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Linux")
        self.assertEqual(len(list(generator.enumerate_jobs())), 68)

        with context_env(CONAN_GCC_VERSIONS="7"):
            self.assertEqual(len(list(generator.enumerate_jobs())), 8)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 4)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_BUILD_TYPES='Debug', CONAN_OPTIONS='build_gmock,shared'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 16)

    def test_total_windows(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Windows")
        self.assertEqual(len(list(generator.enumerate_jobs())), 32)

        with context_env(CONAN_VISUAL_VERSIONS='12'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 8)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 4)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug', CONAN_OPTIONS='build_gmock,shared'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 16)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug', CONAN_VISUAL_RUNTIMES="MT"):
            self.assertEqual(len(list(generator.enumerate_jobs())), 0)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug', CONAN_VISUAL_RUNTIMES="MTd"):
            self.assertEqual(len(list(generator.enumerate_jobs())), 2)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 0)

    def test_filter_jobs(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Windows")
        self.assertEqual(len(list(generator.enumerate_jobs())), 32)

        with context_env(CONAN_VISUAL_VERSIONS='12'):
            all_jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(all_jobs), 8)

            def discard_arch_x86(compiler, options):
                return compiler.arch == 'x86'

            x86_discarded = list(JobGeneratorEnviron.filter_jobs(all_jobs, filter=discard_arch_x86))
            self.assertEqual(len(x86_discarded), 4)

    def test_pagination(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Windows")
        with context_env(CONAN_VISUAL_VERSIONS='12'):
            all_jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(all_jobs), 8)

            page_list = JobGeneratorEnviron.paginate(all_jobs, page=1, page_size=5)
            self.assertEqual(len(page_list), 3)

            page_list = JobGeneratorEnviron.paginate(all_jobs, page=6, page_size=5)
            self.assertEqual(len(page_list), 0)



