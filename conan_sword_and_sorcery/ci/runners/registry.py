# -*- coding: utf-8 -*-

import logging
import os

log = logging.getLogger(__name__)


class RunnerRegistry(object):
    _registry = {}

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
    def get_runner(cls, conanfile, *args, **kwargs):
        log.debug("RunnerRegistry::get_runner()")
        runner = None
        for key, runner_class in cls._registry.items():
            if os.environ.get(key, False):
                runner = runner_class(conanfile=conanfile, *args, **kwargs)
                return runner

        if not runner:
            # TODO: Fallback to a local runner?
            raise ValueError("Runner not found: no environment variable is registered from available ones ('{}')".format("', '".join(cls._registry.keys())))
