# -*- coding: utf-8 -*-
import unittest

from conan_sword_and_sorcery.utils.conan import remote, conf
from conan_sword_and_sorcery.parsers.conan_conf import ConanConf
from tests.utils import parse_remote_list


class TestRemote(unittest.TestCase):
    def setUp(self):
        self.remotes = parse_remote_list()

    def test_remote(self):
        remote_name = 'remote_name'
        remote_url = 'http://my.remote.com'
        with remote(url=remote_url, name=remote_name):
            remotes = dict(parse_remote_list())
            self.assertIn(remote_name, remotes.keys())
            self.assertEqual(remotes[remote_name], remote_url)
        remotes = dict(parse_remote_list())
        self.assertNotIn(remote_name, remotes.keys())

    def test_insert_first(self):
        remote_name = 'remote_name'
        remote_url = 'http://my.remote.com'
        with remote(url=remote_url, name=remote_name, insert_first=True):
            name, url = parse_remote_list()[0]
            self.assertEqual(name, remote_name)
            self.assertEqual(url, remote_url)


class TestConf(unittest.TestCase):
    def test_invalid_file(self):
        with self.assertRaises(RuntimeError):
            with conf(new_values=None, conan_conf="invalid-file") as _:
                self.assertTrue(True)

    def test_conf(self):
        original_conf = ConanConf()
        with self.assertRaises(KeyError):
            original_conf.get(section='log', item="VAR")

        with conf(new_values=(('log', "VAR", "VALUE"),), conan_conf=original_conf.filepath) as new_conf:
            self.assertEqual(new_conf['log']["VAR"], "VALUE")
            conan_conf = ConanConf(filepath=original_conf.filepath)
            self.assertEqual(conan_conf.get(section='log', item="VAR"), "VALUE")

        with self.assertRaises(KeyError):
            conan_conf = ConanConf(filepath=original_conf.filepath)
            conan_conf.get(section='log', item="VAR")
