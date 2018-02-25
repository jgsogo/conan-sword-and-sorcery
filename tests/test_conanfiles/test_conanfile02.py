# -*- coding: utf-8 -*-

import os
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.job_generators.environ_generator import JobGeneratorEnviron
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.parsers.conanfile import ConanFileWrapper
from conan_sword_and_sorcery.ci.compilers import NoCompiler
from tests.utils import TestCaseEnvClean
from conan_sword_and_sorcery.utils.environ import context_env


class TestConanfile02(TestCaseEnvClean):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        conanfile = os.path.join(single_files, 'conanfile02.py')
        self.wrapper = ConanFileWrapper.parse(conanfile)
        self.settings = get_settings()

    def test_total_linux(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Linux")
        self.assertEqual(len(list(generator.enumerate_jobs())), 1)

        with context_env(CONAN_OPTIONS='shared'):
            all_jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(all_jobs), 2)
            self.assertTrue(isinstance(all_jobs[0][0], NoCompiler))
            self.assertTrue(isinstance(all_jobs[1][0], NoCompiler))

        with context_env(CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1)

    def test_total_windows(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Windows")
        self.assertEqual(len(list(generator.enumerate_jobs())), 1)

        with context_env(CONAN_OPTIONS='shared'):
            all_jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(all_jobs), 2)
            self.assertTrue(isinstance(all_jobs[0][0], NoCompiler))
            self.assertTrue(isinstance(all_jobs[1][0], NoCompiler))

        with context_env(CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_VISUAL_VERSIONS='4.7'):
            self.assertEqual(len(list(generator.enumerate_jobs())), 1)

    def test_filter_jobs(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Windows")
        self.assertEqual(len(list(generator.enumerate_jobs())), 1)

        with context_env(CONAN_OPTIONS='shared'):
            all_jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(all_jobs), 2)

            def discard_arch_x86(compiler, options):
                self.assertTrue(isinstance(compiler, NoCompiler))
                return compiler.arch == 'x86'

            x86_discarded = JobGeneratorEnviron.filter_jobs(all_jobs, filter=discard_arch_x86)
            self.assertEqual(len(list(x86_discarded)), 0)

    def test_pagination(self):
        generator = JobGeneratorEnviron(conanfile_wrapper=self.wrapper, settings=self.settings, osys="Windows")
        self.assertEqual(len(list(generator.enumerate_jobs())), 1)

        with context_env(CONAN_OPTIONS='shared'):
            all_jobs = list(generator.enumerate_jobs())
            self.assertEqual(len(all_jobs), 2)

            page_list = JobGeneratorEnviron.paginate(all_jobs, page=0, page_size=10)
            self.assertEqual(len(page_list), 2)

            page_list = JobGeneratorEnviron.paginate(all_jobs, page=1, page_size=10)
            self.assertEqual(len(page_list), 0)



