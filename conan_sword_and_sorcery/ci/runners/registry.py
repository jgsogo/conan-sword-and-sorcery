# -*- coding: utf-8 -*-

import logging
import os

from conan_sword_and_sorcery.ci.runners.base_runner import BaseRunner

log = logging.getLogger(__name__)


class RunnerRegistry(object):
    _registry = {}
    _fallback = None

    @classmethod
    def register(cls, env_variable):
        def real_decorator(runner_class):
            log.debug("RunnerRegistry::register: {})".format(runner_class))
            if env_variable in cls._registry:
                raise ValueError("CI Runner with env_variable='{}' already registered".format(env_variable))
            cls._registry[env_variable] = runner_class
            return runner_class
        return real_decorator

    @classmethod
    def fallback(cls, runner_class):
        if cls._fallback:
            raise RuntimeError("Trying to register '{}' as fallback, but it is already set ('{}')".format(runner_class, cls._fallback))
        cls._fallback = runner_class
        return runner_class

    @classmethod
    def get_runner(cls, conanfile, *args, **kwargs):  # type: (str, Any, Any) -> BaseRunner
        log.debug("RunnerRegistry::get_runner()")
        for key, runner_class in cls._registry.items():
            if os.environ.get(key, False):
                runner = runner_class(conanfile=conanfile, *args, **kwargs)
                return runner

        log.info("Will use fallback runner: '{}'".format(cls._fallback))
        return cls._fallback(conanfile=conanfile, *args, **kwargs)
