# -*- coding: utf-8 -*-

import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.runners import TravisRunner
from conan_sword_and_sorcery.ci.runners.base_runner import DRY_RUN, SUCCESS, FAIL
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.utils.environ import context_env
from conan_sword_and_sorcery.parsers.profile import profile_for
from tests.utils import TestCaseEnvClean


class DockerHelperMocked:
    def __init__(self, dry_run=False, *args, **kwargs):
        self.dry_run = dry_run

    def pull(self):
        pass

    def add_mount_unit(self, host, target):
        pass

    def run(self, allocate_tty=True):
        return DRY_RUN if self.dry_run else FAIL

    def run_in_docker(self, command, sudo=True):
        # TODO: Append commands and check the expected sequence
        pass

    def copy(self, origin, tgt):
        pass


@mock.patch('conan_sword_and_sorcery.ci.runners.mixins._docker.DockerHelper', side_effect=DockerHelperMocked)
class TestTravisRunnerWithDocker(TestCaseEnvClean):
    _initial_context_env = {'CONAN_DOCKER_IMAGE': "docker/jgsogo-image"}

    def setUp(self):
        self.settings = get_settings()
        # Dummy (but valid) conanfile
        me = os.path.dirname(__file__)
        self.conanfile = os.path.join(me, '..', '..', 'files', 'single', 'conanfile01.py')

    def test_dry_run(self, DockerHelperMocked):
        runner = TravisRunner(conanfile=self.conanfile, settings=self.settings, osys="Linux", dry_run=True)
        with context_env(CONAN_GCC_VERSIONS="6", CONAN_ARCHS='x86', CONAN_BUILD_PACKAGES='pckg1', CONAN_SWORD_AND_SORCERY_ITS_ME="true"):
            compiler, options = list(runner.enumerate_jobs())[0]
            with profile_for(compiler=compiler) as profile_file:
                runner.set_compiler(compiler)
                runner.set_profile(profile_file)
                r = runner.run(options={'shared': True}, username='test', channel='testing')
                self.assertEqual(r, DRY_RUN)

    def test_run_fail(self, DockerHelperMocked):
        runner = TravisRunner(conanfile=self.conanfile, settings=self.settings, osys="Linux")
        with context_env(CONAN_GCC_VERSIONS="6", CONAN_ARCHS='x86', CONAN_BUILD_PACKAGES='pckg1'):
            compiler, options = list(runner.enumerate_jobs())[0]
            with profile_for(compiler=compiler) as profile_file:
                runner.set_compiler(compiler)
                runner.set_profile(profile_file)
                r = runner.run(options={'shared': True}, username='test', channel='testing')
                self.assertEqual(r, FAIL)

    def test_upload(self, DockerHelperMocked):
        runner = TravisRunner(conanfile=self.conanfile, settings=self.settings, osys="Linux")
        with context_env(CONAN_GCC_VERSIONS="6", CONAN_ARCHS='x86', CONAN_BUILD_PACKAGES='pckg1'):
            compiler, options = list(runner.enumerate_jobs())[0]
            with profile_for(compiler=compiler) as profile_file:
                runner.set_compiler(compiler)

                with mock.patch('conan_sword_and_sorcery.ci.runners.base_runner.upload', return_value=0) as mocked_upload:
                    with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="True", TRAVIS_BRANCH='non-stable-branch'):
                        runner.upload(username='test', channel='testing')
                    with context_env(CONAN_UPLOAD_ONLY_WHEN_STABLE="False", TRAVIS_BRANCH='non-stable-branch'):
                        runner.upload(username='test', channel='testing')
                        args, kwargs = mocked_upload.call_args
                        self.assertEqual(kwargs['username'], 'test')