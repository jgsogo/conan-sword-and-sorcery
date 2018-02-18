# -*- coding: utf-8 -*-

import os
import unittest
import tempfile

from conan_sword_and_sorcery.parsers.conan_conf import ConanConf


class TestParserConanConf(unittest.TestCase):

    def run(self, *args, **kwargs):
        try:
            tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
            with open(os.path.join(os.path.expanduser("~"), '.conan', 'conan.conf')) as f:
                tmp.write(f.read())
            tmp.close()
            self.conan_conf_filename = tmp.name
            super(TestParserConanConf, self).run(*args, **kwargs)
        finally:
            os.unlink(tmp.name)

    def test_basic(self):
        config = ConanConf(self.conan_conf_filename)
        self.assertIsInstance(config, ConanConf)

    def test_change_storage(self):
        config = ConanConf(self.conan_conf_filename)
        pre = config.get("storage", "path")
        post = "other_path"
        config.replace("storage", "path", post)

        # Storage is changed
        self.assertEqual(config.get("storage", "path"), post)
        config2 = ConanConf(self.conan_conf_filename)
        self.assertEqual(config2.get("storage", "path"), post)

        # It is preserved for the second one
        del config2
        self.assertEqual(config.get("storage", "path"), post)

        # But it is restored for the first one
        del config
        config3 = ConanConf(self.conan_conf_filename)
        self.assertEqual(config3.get("storage", "path"), pre)


if __name__ == '__main__':
    unittest.main()
