# -*- coding: utf-8 -*-
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.utils.cmd import cmd


class TestCMD(unittest.TestCase):

    @mock.patch('os.system', return_value=0)
    def test_success(self, os_system):
        cmd(command="mycommand")
        os_system.assert_called_once_with('mycommand')

    @mock.patch('os.system', return_value=0)
    def test_success_secret(self, os_system):
        cmd(command="mycommand", secret=True)
        os_system.assert_called_once_with('mycommand')

    @mock.patch('os.system', return_value=-1)
    def test_fail(self, os_system):
        with self.assertRaisesRegexp(RuntimeError, "Error running command 'mycommand'"):
            cmd(command="mycommand")
            os_system.assert_called_once_with('mycommand')

    @mock.patch('os.system', return_value=-1)
    def test_fail_secret(self, os_system):
        with self.assertRaisesRegexp(RuntimeError, r"Error running command '\*\*secret\*\*'"):
            cmd(command="mycommand", secret=True)
            os_system.assert_called_once_with('mycommand')

    @mock.patch('os.system', return_value=-1)
    def test_custom_exception(self, os_system):
        with self.assertRaises(IndexError):
            cmd(command="mycommand", exception=IndexError)
            os_system.assert_called_once_with('mycommand')

    @mock.patch('os.system', return_value=-1)
    def test_no_exception(self, os_system):
        r = cmd(command="mycommand", exception=None)
        os_system.assert_called_once_with('mycommand')
        self.assertEqual(r, -1)

    @mock.patch('os.system', return_value=-1)
    def test_custom_message(self, os_system):
        with self.assertRaisesRegexp(RuntimeError, r"Custom mesage '\*\*secret\*\*'"):
            cmd(command="mycommand", secret=True, error_msg="Custom mesage '{command}'")
            os_system.assert_called_once_with('mycommand')


