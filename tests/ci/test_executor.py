# -*- coding: utf-8 -*-

import os
import unittest
import platform
from unittest import mock
from collections import defaultdict

from conan.ci.compilers import Compiler
from conan.ci.settings import get_settings
from conan.ci.Executor import Executor


class TestExecutor(unittest.TestCase):
    def setUp(self):
        import logging
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(level=logging.INFO)

        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        self.conanfile01 = os.path.join(single_files, 'conanfile01.py')

    def test_total(self):
        platform.system = mock.Mock(return_value="Linux")
        executor = Executor(self.conanfile01)

        jobs = list(executor.enumerate_jobs())
        print(len(jobs))

