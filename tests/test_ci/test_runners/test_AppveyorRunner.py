# -*- coding: utf-8 -*-

import os
import unittest

from conan_sword_and_sorcery.ci.runners import AppveyorRunner
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.utils.environ import context_env
from tests.utils import TestCaseEnvClean


class TestAppveyorRunner(TestCaseEnvClean):

    def setUp(self):
        settings = get_settings()
        # Dummy (but valid) conanfile
        me = os.path.dirname(__file__)
        conanfile = os.path.join(me, '..', '..', 'files', 'single', 'conanfile01.py')
        self.runner = AppveyorRunner(conanfile=conanfile, settings=settings, osys="Windows")

    def test_is_pull_request(self):
        self.assertFalse(self.runner.is_pull_request())
        with context_env(APPVEYOR_PULL_REQUEST_NUMBER='23'):
            self.assertTrue(self.runner.is_pull_request())

    def test_is_stable_branch(self):
        with self.assertRaises(TypeError):
            self.runner.is_stable_branch()

        # Appveyor always inform about branch name
        with context_env(APPVEYOR_REPO_BRANCH='master'):
            self.assertFalse(self.runner.is_stable_branch())
        with context_env(APPVEYOR_REPO_BRANCH='stable/v1.2.3'):
            self.assertTrue(self.runner.is_stable_branch())
