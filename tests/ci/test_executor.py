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
        log = logging.getLogger('conan')
        logging.basicConfig()
        log.setLevel(level=logging.DEBUG)

        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', 'files', 'single')
        conanfile01 = os.path.join(single_files, 'conanfile01.py')

        platform.system = mock.Mock(return_value="Linux")
        self.executor = Executor(conanfile01)
        self.executor.enumerate_jobs()

    def test_total(self):
        pass