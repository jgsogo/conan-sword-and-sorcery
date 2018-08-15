# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from collections import namedtuple

from conan_sword_and_sorcery.uploader import upload
from conan_sword_and_sorcery.utils.environ import context_env


class TestUpload(unittest.TestCase):
    Recipe = namedtuple('Recipe', ['name', 'version', ])

    def setUp(self):
        self.recipe = self.Recipe(name="recipe", version="1.2.3")

    def test_no_remote(self):
        self.assertEqual(upload(recipe=self.recipe, username="test", channel="testing"), None)

    def test_no_credentials(self):
        with context_env(CONAN_UPLOAD="https://my.remote.com"):
            with self.assertRaises(ValueError):
                upload(recipe=self.recipe, username="test", channel="testing")

    @mock.patch("conan_sword_and_sorcery.uploader.conan.remote_auth", return_value=None)
    def test_upload_dry_run(self, remote_auth_mocked):
        with context_env(CONAN_UPLOAD='http://my.remote.com', CONAN_USERNAME="test", CONAN_PASSWORD="****"):
            upload(recipe=self.recipe, username="test", channel="testing", dry_run=True)

    @mock.patch("conan_sword_and_sorcery.uploader.conan.remote_auth", return_value=None)
    @mock.patch("conan_sword_and_sorcery.uploader.cmd", return_value=None)
    def test_upload(self, remote_auth_mocked, cmd_mocked):
        with context_env(CONAN_UPLOAD='http://my.remote.com', CONAN_USERNAME="test", CONAN_PASSWORD="****"):
            upload(recipe=self.recipe, username="test", channel="testing", dry_run=False)
