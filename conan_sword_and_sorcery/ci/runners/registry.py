# -*- coding: utf-8 -*-

import itertools
import logging
import os
import tempfile
from collections import defaultdict
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler
from conan_sword_and_sorcery.ci.runners.base_runner import BaseRunner
from conan_sword_and_sorcery.utils import isstr

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
    def get_runner(cls, compiler):
        log.debug("RunnerRegistry::get_runner()")
        runner = None
        for key, runner_class in cls._registry.items():
            if os.environ.get(key, False):
                runner = runner_class(compiler)
                break
        if not runner:
            raise ValueError("Runner not found: no environment variable is registered from available ones ('{}')".format("', '".join(cls._registry.keys())))

        try:
            # Create profile file
            tmp, path = tempfile.mkstemp()
            #tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write("include(default)\n\n")  # Profile 'default'
            tmp.write("[settings]\n")
            compiler.populate_profile_settings(tmp)
            tmp.write("[options]\n[build_requires]\n[env]\n")  # TODO: Is it needed?
            tmp.close()

            # Add profile to runner cli
            runner.set_profile_file(path)
            yield runner
        finally:
            os.remove(tmp.name)
