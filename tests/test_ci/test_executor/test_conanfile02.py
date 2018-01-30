# -*- coding: utf-8 -*-

import os
import unittest
import platform
try:
    from unittest import mock
except ImportError:
    import mock

from conan.ci.Executor import Executor
from tests.utils import context_env


class TestConanfile02(unittest.TestCase):
    def setUp(self):
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', '..', 'files', 'single')
        conanfile = os.path.join(single_files, 'conanfile02.py')
        self.executor = Executor(conanfile)

    def test_total_linux(self):
        platform.system = mock.Mock(return_value="Linux")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 224)

        with context_env(CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 112)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 64)

    def test_total_windows(self):
        platform.system = mock.Mock(return_value="Windows")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 192)

        with context_env(CONAN_BUILD_TYPES='Debug'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 96)

        with context_env(CONAN_BUILD_TYPES='Debug', CONAN_GCC_VERSIONS='4.7'):
            self.assertEqual(len(list(self.executor.enumerate_jobs())), 96)

    def test_filter_jobs(self):
        platform.system = mock.Mock(return_value="Windows")
        self.assertEqual(len(list(self.executor.enumerate_jobs())), 192)

        def discard_arch_x86(compiler, settings, options, *args, **kwargs):
            return settings.get('arch') == 'x86'

        x86_discarded = list(self.executor.filter_jobs(filter=discard_arch_x86))
        self.assertEqual(len(x86_discarded), 96)

    def test_pagination(self):
        platform.system = mock.Mock(return_value="Windows")
        all_jobs = list(self.executor.enumerate_jobs())
        self.assertEqual(len(all_jobs), 192)

        page_list = self.executor.paginate(page=1, page_size=10)
        self.assertEqual(len(page_list), 10)

        page_list = self.executor.paginate(page=19, page_size=10)
        self.assertEqual(len(page_list), 2)



