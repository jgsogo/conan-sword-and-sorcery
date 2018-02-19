# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


class ConanConf(object):
    def __init__(self, filepath=None):
        self.config = ConfigParser()
        self.filepath = filepath or os.path.join(os.path.expanduser("~"), '.conan', 'conan.conf')
        self.config.read(self.filepath)

    def get(self, section, item):
        return self.config[section][item]

