# -*- coding: utf-8 -*-

import os
import itertools
import logging
import platform
from collections import defaultdict

from conans.util.env_reader import get_env
from conan.utils import isstr
from conan.ci.compilers import Compiler
from conans.model.settings import Settings as ConanSettings

log = logging.getLogger(__name__)


class Settings:

    def __init__(self, settings_filename=None):
        filename = settings_filename or os.path.join(os.path.dirname(__file__), '..', 'conan_settings.yaml')
        with open(filename, 'r') as f:
            self.conan_settings = ConanSettings.loads(f.read())

    def current(self, os_system, compiler, arch, build_type, version, **kwargs):
        self.conan_settings.os = os_system
        self.conan_settings.arch = arch
        self.conan_settings.build_type = build_type
        self.conan_settings.compiler = compiler.compiler
        self.conan_settings.compiler.version = version
        return self.conan_settings


def get_settings(os_system=None):
    operating_system = os_system or platform.system()
    compiler_classes = Compiler._registry[operating_system]
    configurations = set(itertools.chain(*[c._configurations for c in compiler_classes]))
    log.debug("get_settings - configurations: {}".format(', '.join(configurations)))

    cross_configs = []
    for compiler_class in compiler_classes:
        compiler = compiler_class()
        r = [[compiler, ], ]  # List of lists
        for config in configurations:
            value = getattr(compiler, config, [None])

            # Make a list
            if isstr(value):
                value = [value, ]
            elif not hasattr(value, '__iter__'):
                value = [value, ]

            r.append(value)
        cross_configs += list(itertools.product(*r))

    for cross_config in cross_configs:
        yield operating_system, cross_config[0], {key: value for key, value in zip(configurations, cross_config[1:])}


