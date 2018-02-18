# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


class ConanConf(object):
    # TODO: Implement this class

    def __init__(self, filepath=None, backup=True):
        self.config = ConfigParser()
        self.filepath = filepath or os.path.join(os.path.expanduser("~"), '.conan', 'conan.conf')
        if backup:
            with open(self.filepath, 'rb') as f:
                self._backup = f.read()
        self.config.read(self.filepath)

    def __del__(self):
        if self._backup:
            with open(self.filepath, 'wb') as f:
                f.write(self._backup)

    def get(self, section, item):
        return self.config[section][item]

    def replace(self, section, item, new_value):
        self.config[section][item] = new_value
        with open(self.filepath, 'w') as f:
            self.config.write(f)

