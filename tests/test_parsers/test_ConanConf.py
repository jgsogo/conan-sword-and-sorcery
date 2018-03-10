# -*- coding: utf-8 -*-

import os
import unittest
import tempfile

from conan_sword_and_sorcery.parsers.conan_conf import ConanConf
from conan_sword_and_sorcery.utils import backup_file


class TestParserConanConf(unittest.TestCase):

    def run(self, *args, **kwargs):
        # TODO: A lot better if we start from a synthetic conan.conf file
        self.conan_conf = os.path.join(os.path.expanduser("~"), '.conan', 'conan.conf')
        with backup_file(self.conan_conf):
            super(TestParserConanConf, self).run(*args, **kwargs)

    def test_basic(self):
        config = ConanConf(self.conan_conf)
        self.assertIsInstance(config, ConanConf)

    def test_storage_path(self):
        config = ConanConf(self.conan_conf)
        path = os.path.expanduser(config.get('storage', 'path'))
        self.assertTrue(os.path.isdir(path), msg="{} is not a directory".format(path))


if __name__ == '__main__':
    unittest.main()
