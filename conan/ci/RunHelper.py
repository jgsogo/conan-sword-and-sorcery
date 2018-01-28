# -*- coding: utf-8 -*-


import platform
from conans.util.env_reader import get_env


class RunHelper(object):
    """
    Wrapper to access environment variables and configuration for each CI system
    """

    default_archs = ["x86", "x86_64"]
    default_build_types = ["Release", "Debug"]

    @property
    def os(self):
        return platform.system()

    @property
    def archs(self):
        return get_env("CONAN_ARCHS", self.default_archs)

    @property
    def build_types(self):
        return get_env("CONAN_BUILD_TYPES", self.default_build_types)

    @property
    def compiler(self):
        raise NotImplementedError()
