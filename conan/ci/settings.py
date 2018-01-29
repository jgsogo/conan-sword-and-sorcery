# -*- coding: utf-8 -*-

import itertools
import logging
from collections import defaultdict

from conans.util.env_reader import get_env
from conan.ci.operating_system import OperatingSystem
from conan.utils import isstr
from conan.ci.compilers import Compiler

log = logging.getLogger(__name__)


def get_settings(os_system=None):
    operating_system = os_system or OperatingSystem()
    compiler_classes = Compiler._registry[operating_system.os]
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


