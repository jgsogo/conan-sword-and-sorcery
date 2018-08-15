# -*- coding: utf-8 -*-

import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.runners import TravisRunner
from conan_sword_and_sorcery.ci.runners.base_runner import SUCCESS
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.utils.environ import context_env
from tests.utils import TestCaseEnvClean


class TestTravisRunner(TestCaseEnvClean):

    def setUp(self):
        settings = get_settings()
        # Dummy (but valid) conanfile
        me = os.path.dirname(__file__)
        conanfile = os.path.join(me, '..', '..', 'files', 'single', 'conanfile01.py')
        self.runner = TravisRunner(conanfile=conanfile, settings=settings, osys="Linux")

    def test_is_pull_request(self):
        with self.assertRaises(AssertionError):
            self.assertFalse(self.runner.is_pull_request())

        # Travis always populates this variable
        with context_env(TRAVIS_PULL_REQUEST='23'):
            self.assertTrue(self.runner.is_pull_request())
        with context_env(TRAVIS_PULL_REQUEST='false'):
            self.assertFalse(self.runner.is_pull_request())

    def test_is_stable_branch(self):
        with self.assertRaises(TypeError):
            self.runner.is_stable_branch()

        # Travis always inform about branch name
        with context_env(TRAVIS_BRANCH='master'):
            self.assertFalse(self.runner.is_stable_branch())
        with context_env(TRAVIS_BRANCH='stable/v1.2.3'):
            self.assertTrue(self.runner.is_stable_branch())

    @mock.patch('conan_sword_and_sorcery.ci.runners.base_runner.cmd', return_value=0)
    def test_cmd(self, cmd_mocked):
        self.assertEqual(self.runner.cmd(command="mycommand"), SUCCESS)
