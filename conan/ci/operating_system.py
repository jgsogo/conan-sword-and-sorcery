# -*- coding: utf-8 -*-
import platform

from conans.util.env_reader import get_env


class OperatingSystem(object):
    @property
    def os(self):
        return platform.system()

    @property
    def archs(self):
        return get_env("CONAN_ARCHS", ["x86", "x86_64"])