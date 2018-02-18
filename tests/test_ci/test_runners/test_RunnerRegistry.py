# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.runners import RunnerRegistry, TravisRunner, AppveyorRunner
from tests.utils import context_env, TestCaseEnvClean


class TestRunnerRegistry(TestCaseEnvClean):

    def setUp(self):
        self.registry = RunnerRegistry()
        self.os = ["Windows", "Linux", "Macos",]

    def test_none(self):
        with self.assertRaises(ValueError):
            self.registry.get_runner(conanfile=None)

    def test_travis(self):
        with context_env(TRAVIS='True'):
            runner = self.registry.get_runner(conanfile=None, recipe=None)
            self.assertIsInstance(runner, TravisRunner)

    def test_appveyor(self):
        with context_env(APPVEYOR='True'):
            runner = self.registry.get_runner(conanfile=None, recipe=None)
            self.assertIsInstance(runner, AppveyorRunner)
