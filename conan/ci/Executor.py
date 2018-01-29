# -*- coding: utf-8 -*-

from .settings import get_settings


class Executor(object):
    def __init__(self, settings, conanfile):
        self.settings = settings
        self.conanfile = conanfile

