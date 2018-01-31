# -*- coding: utf-8 -*-

from conan.utils import isstr


class BaseCompiler:
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

    @classmethod
    def validate(self, **kwargs):
        # Raise error if given configuration is not supported
        return True

    @classmethod
    def environment_filters(cls):
        raise NotImplementedError