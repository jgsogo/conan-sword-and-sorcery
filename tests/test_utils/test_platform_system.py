# -*- coding: utf-8 -*-
import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.utils import platform_system


class TestPlatformSystem(unittest.TestCase):

    @mock.patch('conan_sword_and_sorcery.utils.platform.system')
    def test_windows(self, platform_system_mock):
        platform_system_mock.return_value = "Windows"
        self.assertEqual(platform_system(), "Windows")

    @mock.patch('conan_sword_and_sorcery.utils.platform.system')
    def test_windows(self, platform_system_mock):
        platform_system_mock.return_value = "Darwin"
        self.assertEqual(platform_system(), "Macos")
