# -*- coding: utf-8 -*-

import itertools
import logging
from collections import defaultdict
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler
from conan_sword_and_sorcery.utils import isstr

log = logging.getLogger(__name__)


def _raise_on_difference(lhs, rhs, msg="Some items are in 'lhs' but not in 'rhs': '{z}'"):
    z = list(set(lhs) - set(rhs))
    if z:
        raise ValueError(msg.format(z=z))


class CompilerClassHolder(object):
    def __init__(self, compiler_class, **kwargs):
        assert(issubclass(compiler_class, BaseCompiler))
        self.compiler_class = compiler_class
        self.configurations = kwargs

    def __str__(self):
        return self.compiler_class.__name__

    def environment_filters(self):
        return self.compiler_class.environment_filters()

    def get_configurations(self, key):
        return self.configurations.get(key)

    def explode(self, **configurations):
        log.debug("CompilerClassHolder::explode(configurations='{}')".format(configurations))
        explode_vector = []
        _raise_on_difference(configurations.keys(), self.configurations.keys(), msg="Some configurations required are not registered: '{z}'")
        for key, values in self.configurations.items():
            explode_filter = configurations.get(key, values)
            _raise_on_difference(explode_filter, values, msg="Some configurations required for '{}' are not found: '{{z}}'".format(key))
            explode_vector.append(explode_filter)

        for pack in itertools.product(*explode_vector):
            args_dict = {key: value for key, value in zip(self.configurations.keys(), pack)}
            if self.compiler_class.validate(**args_dict):
                log.debug(" - validated config: {}".format(args_dict))
                yield self.compiler_class(**args_dict)
        return


class CompilerRegistry(object):
    _registry = []

    @classmethod
    def environment_filters(cls):
        env_filters = defaultdict(set)
        for holder in cls._registry:
            for key, values in holder.environment_filters().items():
                env_filters[key].update(values)
        return env_filters

    @classmethod
    def register(cls, **kwargs):
        def real_decorator(compiler_class):
            log.debug("CompilerRegistry::register: {})".format(compiler_class))
            cls._registry.append(CompilerClassHolder(compiler_class, **kwargs))
            return compiler_class
        return real_decorator

    @classmethod
    def get_compilers(cls, os=[], version=None, **filters):
        log.debug("CompilerRegistry::get_compilers()")
        filter_keys = list(filters.keys())
        for compiler_holder in cls._registry:
            if compiler_holder.compiler_class.osys not in os:
                continue
            # Filter versions for compiler id.
            if version is not None:
                assert all(not isstr(it) for it in version), "Version should be a list of tuples [('compiler.id', 'version'), ...]"
                filters['version'] = [it[1] for it in version if it[0] == compiler_holder.compiler_class.id]

            try:
                for it in compiler_holder.explode(**filters):
                    yield it
            except ValueError as e:
                log.warning("Compiler {} discarded: {}".format(compiler_holder, e))
        log.debug(" - no compiler found")
        return
