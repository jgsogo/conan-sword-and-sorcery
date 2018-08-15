# -*- coding: utf-8 -*-

import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.runners import RunnerRegistry, TravisRunner, AppveyorRunner, ProfilesRunner
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.utils.environ import context_env
from conan_sword_and_sorcery.utils import platform_system

from tests.utils import TestCaseEnvClean


class TestRunnerRegistry(TestCaseEnvClean):

    def setUp(self):
        self.registry = RunnerRegistry()
        self.settings = get_settings()
        # Dummy (but valid) conanfile
        me = os.path.dirname(__file__)
        single_files = os.path.join(me, '..', '..', 'files', 'single')
        self.conanfile = os.path.join(single_files, 'conanfile01.py')

    def test_none(self):
        runner = self.registry.get_runner(conanfile=self.conanfile, settings=self.settings, osys=platform_system())
        self.assertIsInstance(runner, ProfilesRunner)

    def test_travis(self):
        with context_env(TRAVIS='True'):
            runner = self.registry.get_runner(conanfile=self.conanfile, settings=self.settings, osys='Linux')
            self.assertIsInstance(runner, TravisRunner)

    def test_appveyor(self):
        with context_env(APPVEYOR='True'):
            runner = self.registry.get_runner(conanfile=self.conanfile, settings=self.settings, osys='Windows')
            self.assertIsInstance(runner, AppveyorRunner)

    def test_single_fallback(self):
        with self.assertRaises(RuntimeError):
            @RunnerRegistry.fallback
            class OtherRunner():
                pass

    def test_no_repeated_env_variable(self):
        with self.assertRaises(ValueError):
            @RunnerRegistry.register("APPVEYOR")
            class OtherRunner():
                pass

        with self.assertRaises(ValueError):
            @RunnerRegistry.register("TRAVIS")
            class OtherRunner():
                pass