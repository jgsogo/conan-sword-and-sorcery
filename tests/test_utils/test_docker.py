# -*- coding: utf-8 -*-
import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.utils.docker import DockerHelper, temporary_env_file
from conan_sword_and_sorcery.utils.environ import context_env


class TestTemporaryEnvFile(unittest.TestCase):
    def test_temporary_env_file(self):
        with context_env(CONAN_VAR="conan_var", TRAVIS_VAR="travis_var", APPVEYOR_VAR="appveyor_var"):
            with temporary_env_file() as tmp_file:
                vars = dict([line.strip().split('=') for line in open(tmp_file, 'r').readlines()])
                self.assertIn('CONAN_VAR', vars)
                self.assertEqual(vars['CONAN_VAR'], 'conan_var')
                self.assertIn('TRAVIS_VAR', vars)
                self.assertEqual(vars['TRAVIS_VAR'], 'travis_var')

                self.assertNotIn('APPVEYOR_VAR', vars)  # Docker is available only for TRAVIS


@mock.patch('conan_sword_and_sorcery.utils.docker.cmd', return_value='')
class TestDockerHelper(unittest.TestCase):
    def setUp(self):
        self.helper = DockerHelper(image="conan/jgsogo")

    def test_name(self, mocked_cmd):
        self.assertEqual(self.helper.image, "conan/jgsogo")
        self.assertEqual(self.helper.name, "conan_jgsogo")
        self.assertEqual(mocked_cmd.call_count, 0)

    def test_pull(self, mocked_cmd):
        self.helper.pull()
        args, kwargs = mocked_cmd.call_args
        self.assertEqual(kwargs['command'], "docker pull {}".format(self.helper.image))
        self.assertEqual(mocked_cmd.call_count, 1)

    def test_run_stop(self, mocked_cmd):
        self.assertEqual(self.helper._is_running, False)

        self.helper.run()
        args, kwargs = mocked_cmd.call_args
        self.assertEqual(self.helper._is_running, True)
        self.assertIn('docker run', kwargs['command'])
        self.assertEqual(mocked_cmd.call_count, 1)

        self.helper._stop()
        args, kwargs = mocked_cmd.call_args
        self.assertEqual(self.helper._is_running, False)
        self.assertIn('docker stop', kwargs['command'])
        self.assertEqual(mocked_cmd.call_count, 2)

    def test_already_running(self, mocked_cmd):
        self.assertEqual(self.helper._is_running, False)
        self.helper.run()
        self.assertEqual(mocked_cmd.call_count, 1)

        self.helper.run()  # Stop and run again
        self.assertEqual(mocked_cmd.call_count, 3)

    def test_add_mount_unit(self, mocked_cmd):
        self.helper.add_mount_unit("host", "target")
        self.assertEqual(mocked_cmd.call_count, 0)

        self.helper.add_mount_unit("host", "target2")  # TODO: check for warning!
        self.assertEqual(self.helper.mnt["host"], "target2")
        self.assertEqual(mocked_cmd.call_count, 0)

    def test_add_mount_unit_running(self, mocked_cmd):
        self.helper.run()
        self.assertEqual(mocked_cmd.call_count, 1)
        self.helper.add_mount_unit("host", "target")  # Stop and run again
        self.assertEqual(mocked_cmd.call_count, 3)

    def test_copy(self, mocked_cmd):
        self.helper.copy("origin", "tgt")
        args, kwargs = mocked_cmd.call_args
        self.assertIn('docker cp', kwargs['command'])

    def test_run_in_docker(self, mocked_cmd):
        self.helper.run_in_docker(command="comando", sudo=False)
        args, kwargs = mocked_cmd.call_args
        self.assertIn('docker exec', kwargs['command'])
        self.assertNotIn('sudo', kwargs['command'])

        self.helper.run_in_docker(command="comando", sudo=True)
        args, kwargs = mocked_cmd.call_args
        self.assertIn('sudo', kwargs['command'])
