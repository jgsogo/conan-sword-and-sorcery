# -*- coding: utf-8 -*-

import os
import unittest
import argparse
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.run import main, run
from conan_sword_and_sorcery.ci.compilers.clang import CompilerClangApple
from conan_sword_and_sorcery.ci.runners.base_runner import DRY_RUN, SUCCESS, FAIL
from conan_sword_and_sorcery.utils.environ import context_env
from conan_sword_and_sorcery.utils import backup_file
from tests.utils import parse_remote_list


@mock.patch('argparse.ArgumentParser.parse_args')
class TestMain(unittest.TestCase):

    @mock.patch('conan_sword_and_sorcery.ci.run.run', return_value='mocked')
    def test_main_invalid_conanfile(self, run_mocked, argparse_mocked):
        argparse_mocked.return_value = argparse.Namespace(dry_run=True, conanfile='here', verbose_count=0)
        with self.assertRaises(SystemExit):
            main()

    @mock.patch('conan_sword_and_sorcery.ci.run.run', return_value='mocked')
    def test_main(self, run_mocked, argparse_mocked):
        conanfile = os.path.join(os.path.dirname(__file__), '..', 'files', 'single', 'conanfile01.py')
        argparse_mocked.return_value = argparse.Namespace(dry_run=True, conanfile=conanfile, verbose_count=0, conan_options=None, conan_username=None, conan_channel=None)
        self.assertEqual(main(), "mocked")

    @mock.patch('conan_sword_and_sorcery.ci.run.run')
    def test_main_options(self, run_mocked, argparse_mocked):
        conanfile = os.path.join(os.path.dirname(__file__), '..', 'files', 'single', 'conanfile01.py')
        argparse_mocked.return_value = argparse.Namespace(dry_run=True, conanfile=conanfile, verbose_count=0, conan_options="opt1", conan_username=None, conan_channel=None)

        def check_env(conanfile, dry_run):
            self.assertEqual(dry_run, True)
            self.assertEqual(os.environ['CONAN_OPTIONS'], 'opt1')
            return 'check_env'

        run_mocked.side_effect = check_env
        self.assertEqual(main(), "check_env")

    @mock.patch('conan_sword_and_sorcery.ci.run.run')
    def test_main_username(self, run_mocked, argparse_mocked):
        conanfile = os.path.join(os.path.dirname(__file__), '..', 'files', 'single', 'conanfile01.py')
        argparse_mocked.return_value = argparse.Namespace(dry_run=True, conanfile=conanfile, verbose_count=0, conan_options=None,
                                                          conan_username="username", conan_channel=None)

        def check_env(conanfile, dry_run):
            self.assertEqual(dry_run, True)
            self.assertEqual(os.environ['CONAN_USERNAME'], 'username')
            return 'check_env'

        run_mocked.side_effect = check_env
        self.assertEqual(main(), "check_env")

    @mock.patch('conan_sword_and_sorcery.ci.run.run')
    def test_main_channel(self, run_mocked, argparse_mocked):
        conanfile = os.path.join(os.path.dirname(__file__), '..', 'files', 'single', 'conanfile01.py')
        argparse_mocked.return_value = argparse.Namespace(dry_run=True, conanfile=conanfile, verbose_count=0, conan_options=None,
                                                          conan_username=None, conan_channel="channel")

        def check_env(conanfile, dry_run):
            self.assertEqual(dry_run, True)
            self.assertEqual(os.environ['CONAN_CHANNEL'], 'channel')
            return 'check_env'

        run_mocked.side_effect = check_env
        self.assertEqual(main(), "check_env")


class Runner4Testing:
    def __init__(self, run_return, n_jobs=None):
        self.run_return = run_return
        self.n_jobs = n_jobs

    def enumerate_jobs(self):
        jobs = [(CompilerClangApple(version='4.9', arch='x86', build_type='Release', libcxx='libstdc++11', ), {}),
                (CompilerClangApple(version='4.9', arch='x86_64', build_type='Release', libcxx='libstdc++11', ), {})]
        if self.n_jobs:
            jobs = jobs[:self.n_jobs]
        return jobs

    def is_stable_branch(self):
        return False

    def set_compiler(self, compiler):
        pass

    def set_profile(self, profile_file):
        pass

    def run(self, options, username, channel):
        return self.run_return

    def upload(self, *args, **kwargs):
        pass


class TestRun(unittest.TestCase):
    def run(self, *args, **kwargs):
        with backup_file(os.path.join(os.path.expanduser("~"), '.conan', 'registry.txt')):
            return super(TestRun, self).run(*args, **kwargs)

    def setUp(self):
        self.conanfile = os.path.join(os.path.dirname(__file__), '..', 'files', 'single', 'conanfile01.py')

    @mock.patch('conan_sword_and_sorcery.ci.run.RunnerRegistry.get_runner', return_value=Runner4Testing(run_return=SUCCESS))
    def test_run_success(self, runner_mocked):
        self.assertEqual(run(conanfile=self.conanfile, dry_run=False), 0)

    @mock.patch('conan_sword_and_sorcery.ci.run.RunnerRegistry.get_runner', return_value=Runner4Testing(run_return=FAIL))
    def test_run_fail(self, runner_mocked):
        self.assertEqual(run(conanfile=self.conanfile, dry_run=False), -1)

    @mock.patch('conan_sword_and_sorcery.ci.run.RunnerRegistry.get_runner', return_value=Runner4Testing(run_return=SUCCESS))
    def test_run_pages(self, runner_mocked):
        with context_env(CONAN_TOTAL_PAGES="2", CONAN_CURRENT_PAGE="1", ):
            self.assertEqual(run(conanfile=self.conanfile, dry_run=False), 0)

    @mock.patch('conan_sword_and_sorcery.ci.run.RunnerRegistry.get_runner', return_value=Runner4Testing(run_return=SUCCESS, n_jobs=1))
    def test_run_pages_invalid(self, runner_mocked):
        with context_env(CONAN_TOTAL_PAGES="2", CONAN_CURRENT_PAGE="1", ):
            with self.assertRaises(AssertionError):
                self.assertEqual(run(conanfile=self.conanfile, dry_run=False), 0)

    @mock.patch('conan_sword_and_sorcery.ci.run.RunnerRegistry.get_runner')
    def test_run_remotes(self, runner_mocked):
        initial_remotes = set([it[1] for it in parse_remote_list()])

        class Runner4TestingEnvCheck(Runner4Testing):
            def run(_, options, username, channel):
                remotes = set([it[1] for it in parse_remote_list()])
                self.assertEqual(len(initial_remotes) + 2, len(remotes))
                return SUCCESS

        runner_mocked.return_value = Runner4TestingEnvCheck(run_return=SUCCESS)

        with context_env(CONAN_REMOTES="http://remote1.com,http://remote2.com", CONAN_UPLOAD="http://remote1.com"):
            self.assertEqual(run(conanfile=self.conanfile, dry_run=False), 0)

    @mock.patch('conan_sword_and_sorcery.ci.run.RunnerRegistry.get_runner')
    def test_run_remotes_and_upload(self, runner_mocked):
        initial_remotes = set([it[1] for it in parse_remote_list()])

        class Runner4TestingEnvCheck(Runner4Testing):
            def run(_, options, username, channel):
                remotes = set([it[1] for it in parse_remote_list()])
                self.assertEqual(len(initial_remotes) + 2 + 1, len(remotes))
                return SUCCESS

        runner_mocked.return_value = Runner4TestingEnvCheck(run_return=SUCCESS)

        with context_env(CONAN_REMOTES="http://remote1.com,http://remote2.com", CONAN_UPLOAD="http://remote3.com"):
            self.assertEqual(run(conanfile=self.conanfile, dry_run=False), 0)



