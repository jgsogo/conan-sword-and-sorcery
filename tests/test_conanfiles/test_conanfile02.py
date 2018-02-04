# -*- coding: utf-8 -*-

import os
import unittest
import platform
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.Executor import Executor
from conan_sword_and_sorcery.ci.compilers import NoCompiler
from tests.utils import context_env, TestCaseEnvClean


class TestConanfile02(TestCaseEnvClean):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'conanfile02.py')

    def test_total_linux(self):
        self.executor = Executor(self.conanfile, osys="Linux")
        all_jobs = list(self.executor.enumerate_jobs())
        self.assertEqual(len(all_jobs), 2)
        self.assertTrue(isinstance(all_jobs[0][0], NoCompiler))
        self.assertTrue(isinstance(all_jobs[1][0], NoCompiler))

        with context_env(CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

    def test_total_windows(self):
        self.executor = Executor(self.conanfile, osys="Windows")
        all_jobs = list(self.executor.enumerate_jobs())
        self.assertEqual(len(all_jobs), 2)
        self.assertTrue(isinstance(all_jobs[0][0], NoCompiler))
        self.assertTrue(isinstance(all_jobs[1][0], NoCompiler))

        with context_env(CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

    def test_filter_jobs(self):
        self.executor = Executor(self.conanfile, osys="Windows")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 2)

        def discard_arch_x86(compiler, options):
            self.assertTrue(isinstance(compiler, NoCompiler))
            return compiler.arch == 'x86'

        x86_discarded = list(self.executor.filter_jobs(filter=discard_arch_x86))
        self.assertEqual(len(x86_discarded), 0)

    def test_pagination(self):
        self.executor = Executor(self.conanfile, osys="Windows")
        all_jobs = list(self.executor.enumerate_jobs())
        self.assertEqual(len(all_jobs), 2)

        page_list = self.executor.paginate(page=0, page_size=10)
        self.assertEqual(len(page_list), 2)

        page_list = self.executor.paginate(page=1, page_size=10)
        self.assertEqual(len(page_list), 0)



