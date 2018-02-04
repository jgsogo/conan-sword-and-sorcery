# -*- coding: utf-8 -*-

from conan_sword_and_sorcery.utils import isstr


class BaseCompiler(object):
    id = None
    os = None

    def __init__(self, **kwargs):
        self._data = kwargs

        # Validate input arguments
        for key, val in kwargs.items():
            if not val or not isstr(val):
                raise ValueError("Invalid configuration argument for compiler '{}': argument '{}' must be a non empty string.".format(self.id, key))

    def __getattr__(self, item):
        return self._data.get(item)

    def update_settings(self, settings):
        settings.build_type = self.build_type
        settings.arch = self.arch
        settings.compiler = self.id
        settings.compiler.version = self.version

    @classmethod
    def validate(cls, **kwargs):
        # Raise error if given configuration is not supported
        return True

    @classmethod
    def environment_filters(cls):
        raise NotImplementedError
