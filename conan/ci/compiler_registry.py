# -*- coding: utf-8 -*-

import logging
import itertools

from conans.util.env_reader import get_env

log = logging.getLogger(__name__)


def _raise_on_difference(lhs, rhs, msg="Some items are in 'lhs' but not in 'rhs': '{z}'"):
    z = list(set(lhs) - set(rhs))
    if z:
        raise ValueError(msg.format(z=z))


class CompilerClassHolder:
    def __init__(self, compiler_class, **kwargs):
        self.compiler_class = compiler_class
        self.configurations = kwargs

    def __str__(self):
        return self.compiler_class.__name__

    def get_configurations(self, key):
        return self.configurations.get(key)

    def explode(self, **configurations):
        explode_vector = []
        _raise_on_difference(configurations.keys(), self.configurations.keys(), msg="Some configurations required are not registered: '{{}}'")
        for key, values in self.configurations.items():
            explode_filter = configurations.get(key, values)
            _raise_on_difference(explode_filter, values, msg="Some configurations required for '{}' are not found: '{{z}}'".format(key))
            explode_vector.append(explode_filter)

        for pack in itertools.product(*explode_vector):
            args_dict = {key: value for key, value in zip(self.configurations.keys(), pack)}
            yield self.compiler_class(**args_dict)


class CompilerRegistry:
    _registry = []

    @classmethod
    def register(cls, **kwargs):
        def real_decorator(compiler_class):
            log.debug("CompilerRegistry::register: {})".format(compiler_class))
            cls._registry.append(CompilerClassHolder(compiler_class, **kwargs))
            return compiler_class
        return real_decorator

    @classmethod
    def get_compilers(cls, **filters):
        filter_keys = list(filters.keys())
        for compiler_holder in cls._registry:
            try:
                for it in compiler_holder.explode(**filters):
                    yield it
            except ValueError as e:
                log.warning("Compiler {} discarded: {}".format(compiler_holder, e))
        return


class Compiler:
    def __init__(self, **kwargs):
        pass


@CompilerRegistry.register(
    archs = get_env("CONAN_ARCHS", ["x86", "x86_64"]),
    versions = get_env("CONAN_GCC_VERSIONS", ["4.9", "5", "6", "7"]),
    build_types = get_env("CONAN_BUILD_TYPES", ["Release", "Debug"])
)
class CompilerGCC(Compiler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
