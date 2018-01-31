# -*- coding: utf-8 -*-

from functools import reduce
from operator import mul


class BaseCompiler:
    def __init__(self, name, **kwargs):
        self.name = name
        self._data = kwargs

        # Validate input arguments
        for key, val in kwargs.items():
            if not len(val):
                raise ValueError("Invalid configuration argument for compiler '{}': argument '{}' must be a list.".format(name, key))

    def __getattr__(self, item):
        return getattr(self._data, item)

    def max_configurations(self):
        return reduce(mul, [len(values) for values in self._data.values()], 1)
