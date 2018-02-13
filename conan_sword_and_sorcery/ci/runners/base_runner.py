# -*- coding: utf-8 -*-


class BaseRunner(object):
    profile = None

    def __init__(self, compiler):
        self.compiler = compiler

    def set_profile_file(self, filename):
        self.profile = filename

