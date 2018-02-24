# -*- coding: utf-8 -*-

import os
import unittest
import platform
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.job_generator import JobGenerator
from tests.utils import context_env, TestCaseEnvClean


class TestConanfile01(TestCaseEnvClean):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile01 = os.path.join(single_files, 'conanfile01.py')

    def test_total_macos(self):
        self.executor = JobGenerator(self.conanfile01, osys="Macos")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="7.3"):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 8)

        with context_env(CONAN_APPLE_CLANG_VERSIONS="7.3", CONAN_BUILD_TYPES="Release",
                         CONAN_ARCHS="x86_64"):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

    def test_total_linux(self):
        self.executor = JobGenerator(self.conanfile01, osys="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0)

        with context_env(CONAN_GCC_VERSIONS="7"):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 8)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 4)

        with context_env(CONAN_GCC_VERSIONS="7", CONAN_BUILD_TYPES='Debug', CONAN_OPTIONS='build_gmock,shared'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 16)

    def test_total_windows(self):
        self.executor = JobGenerator(self.conanfile01, osys="Windows")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0)

        with context_env(CONAN_VISUAL_VERSIONS='12'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 8)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 4)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug', CONAN_OPTIONS='build_gmock,shared'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 16)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug', CONAN_VISUAL_RUNTIMES="MT"):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 0)

        with context_env(CONAN_VISUAL_VERSIONS='12', CONAN_BUILD_TYPES='Debug', CONAN_VISUAL_RUNTIMES="MTd"):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 0)

    def test_filter_jobs(self):
        self.executor = JobGenerator(self.conanfile01, osys="Windows")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 0)

        with context_env(CONAN_VISUAL_VERSIONS='12'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 8)

            def discard_arch_x86(compiler, options):
                return compiler.arch == 'x86'

            x86_discarded = list(self.executor.filter_jobs(filter=discard_arch_x86))
            self.assertEqual(len(x86_discarded), 4)

    def test_pagination(self):
        self.executor = JobGenerator(self.conanfile01, osys="Windows")
        with context_env(CONAN_VISUAL_VERSIONS='12'):
            all_jobs = list(self.executor.enumerate_jobs())
            self.assertEqual(len(all_jobs), 8)

            page_list = self.executor.paginate(page=1, page_size=5)
            self.assertEqual(len(page_list), 3)

            page_list = self.executor.paginate(page=6, page_size=5)
            self.assertEqual(len(page_list), 0)



