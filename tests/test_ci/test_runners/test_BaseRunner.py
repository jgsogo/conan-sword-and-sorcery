# -*- coding: utf-8 -*-

import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.runners import AppveyorRunner
from conan_sword_and_sorcery.ci.runners.base_runner import SUCCESS, FAIL, DRY_RUN, BaseRunner
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.utils.environ import context_env
from conan_sword_and_sorcery.parsers.profile import profile_for
from tests.utils import TestCaseEnvClean


class JobGeneratorClass4Testing:
    def __init__(self, *args, **kwargs):
        pass


class BaseRunner4Testing(BaseRunner):
    job_generator_class = JobGeneratorClass4Testing


class TestBaseRunnerStableBranch(TestCaseEnvClean):

    def setUp(self):
        self.settings = get_settings()
        # Dummy (but valid) conanfile
        me = os.path.dirname(__file__)
        self.conanfile = os.path.join(me, '..', '..', 'files', 'single', 'conanfile01.py')

    def test_enumerate_jobs(self):
        runner = AppveyorRunner(conanfile=self.conanfile, settings=self.settings, osys="Windows")
        with context_env(CONAN_VISUAL_VERSIONS="12", CONAN_VISUAL_RUNTIMES="MT"):
            self.assertTrue(len(list(runner.enumerate_jobs())) != 0)

    def test_is_pull_request(self):
        runner = BaseRunner4Testing(conanfile=self.conanfile, settings=self.settings, osys="Windows")
        with self.assertRaises(NotImplementedError):
            runner.is_pull_request()

    def test_get_branch_name(self):
        runner = BaseRunner4Testing(conanfile=self.conanfile, settings=self.settings, osys="Windows")
        with self.assertRaises(NotImplementedError):
            runner.get_branch_name()

    def test_dry_run(self):
        runner = AppveyorRunner(conanfile=self.conanfile, settings=self.settings, osys="Windows", dry_run=True)
        with context_env(CONAN_GCC_VERSIONS="6", CONAN_ARCHS='x86', CONAN_BUILD_PACKAGES='pckg1'):
            compiler, options = list(runner.enumerate_jobs())[0]
            with profile_for(compiler=compiler) as profile_file:
                runner.set_compiler(compiler)
                runner.set_profile(profile_file)
                r = runner.run(options={'shared': True}, username='test', channel='testing')
                self.assertEqual(r, DRY_RUN)

    def test_run_fail(self):
        runner = AppveyorRunner(conanfile=self.conanfile, settings=self.settings, osys="Windows")
        with context_env(CONAN_GCC_VERSIONS="6", CONAN_ARCHS='x86', CONAN_BUILD_PACKAGES='pckg1'):
            compiler, options = list(runner.enumerate_jobs())[0]
            with profile_for(compiler=compiler) as profile_file:
                runner.set_compiler(compiler)
                runner.set_profile(profile_file)

                with mock.patch('conan_sword_and_sorcery.ci.runners.base_runner.cmd', return_value=1) as mocked_cmd:
                    r = runner.run(options={'shared': True}, username='test', channel='testing')
                    self.assertEqual(r, FAIL)

    def test_run_success(self):
        runner = AppveyorRunner(conanfile=self.conanfile, settings=self.settings, osys="Windows")
        with context_env(CONAN_GCC_VERSIONS="6", CONAN_ARCHS='x86', CONAN_BUILD_PACKAGES='pckg1'):
            compiler, options = list(runner.enumerate_jobs())[0]
            with profile_for(compiler=compiler) as profile_file:
                runner.set_compiler(compiler)
                runner.set_profile(profile_file)

                with mock.patch('conan_sword_and_sorcery.ci.runners.base_runner.cmd', return_value=0) as mocked_cmd:
                    r = runner.run(options={'shared': True}, username='test', channel='testing')
                    self.assertEqual(r, SUCCESS)

                    args, kwargs = mocked_cmd.call_args
                    self.assertEqual(len(args), 0)  # All arguments are passed with name
                    self.assertEqual(kwargs['exception'], None)
                    command = kwargs.get('command')
                    self.assertIn('--build=pckg1', command)
                    self.assertIn('--build=outdated', command)
                    self.assertIn('--build={}'.format(runner.recipe.name), command)
                    self.assertIn('--profile {}'.format(profile_file), command)
                    self.assertIn('-o {}:shared=True'.format(runner.recipe.name), command)

    def test_is_upload_requested(self):
        runner = AppveyorRunner(conanfile=self.conanfile, settings=self.settings, osys="Windows")

        with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="True", APPVEYOR_REPO_BRANCH='non-stable-branch'):
            self.assertFalse(runner.is_stable_branch())
            self.assertFalse(runner.is_upload_requested())

        with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="False", APPVEYOR_REPO_BRANCH='non-stable-branch'):
            self.assertFalse(runner.is_stable_branch())
            self.assertTrue(runner.is_upload_requested())

        with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="False", APPVEYOR_REPO_BRANCH='stable/v1.2.3'):
            self.assertTrue(runner.is_stable_branch())
            self.assertTrue(runner.is_upload_requested())

        with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="True", APPVEYOR_REPO_BRANCH='stable/v1.2.3'):
            self.assertTrue(runner.is_stable_branch())
            self.assertTrue(runner.is_upload_requested())

    def test_upload(self):
        runner = AppveyorRunner(conanfile=self.conanfile, settings=self.settings, osys="Windows")
        with mock.patch('conan_sword_and_sorcery.ci.runners.base_runner.upload', return_value=0) as mocked_upload:
            with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="True", APPVEYOR_REPO_BRANCH='non-stable-branch'):
                runner.upload(username='test', channel='testing')
            with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="False", APPVEYOR_REPO_BRANCH='non-stable-branch'):
                runner.upload(username='test', channel='testing')
                args, kwargs = mocked_upload.call_args
                self.assertEqual(kwargs['username'], 'test')
