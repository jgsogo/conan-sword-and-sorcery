# -*- coding: utf-8 -*-

import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.runners import RunnerRegistry, TravisRunner, AppveyorRunner, ProfilesRunner
from conan_sword_and_sorcery.parsers.settings import get_settings
from tests.utils import TestCaseEnvClean
from conan_sword_and_sorcery.utils.environ import context_env


class TestRunnerRegistry(TestCaseEnvClean):

    def setUp(self):
        self.registry = RunnerRegistry()
        self.settings = get_settings()
        # Dummy (but valid) conanfile
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'conanfile01.py')

    def test_none(self):
        runner = self.registry.get_runner(conanfile=self.conanfile, settings=self.settings, osys='Windows')
        self.assertIsInstance(runner, ProfilesRunner)

    def test_travis(self):
        with context_env(TRAVIS='True'):
            runner = self.registry.get_runner(conanfile=self.conanfile, settings=self.settings, osys='Linux')
            self.assertIsInstance(runner, TravisRunner)

    def test_appveyor(self):
        with context_env(APPVEYOR='True'):
            runner = self.registry.get_runner(conanfile=self.conanfile, settings=self.settings, osys='Windows')
            self.assertIsInstance(runner, AppveyorRunner)
