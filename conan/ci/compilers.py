# -*- coding: utf-8 -*-

import itertools
import platform
from collections import defaultdict
from conans.util.env_reader import get_env

from conan.utils import isstr

_registry_by_os = defaultdict(list)


def register(compiler):
    _registry_by_os[compiler.os_system].append(compiler)
    return compiler


def get_compilers(os_system):
    return _registry_by_os[os_system]


def get_available_configurations(compiler_classes=None):
    compiler_classes = compiler_classes or get_compilers(platform.system())
    cross_config = []
    for compiler_class in compiler_classes:
        compiler = compiler_class()
        r = []
        for config in compiler._configurations:
            values = getattr(compiler, config)
            # Make a list
            if isstr(values):
                values = [values, ]
            elif not hasattr(values, '__iter__'):
                values = [values, ]
            r.append(values)

        compiler_configurations = []
        for config_cross in itertools.product(*r):
            compiler_configurations.append({key: value for key, value in zip(compiler._configurations, config_cross)})

        cross_config.append((compiler, compiler_configurations))
    return cross_config


class Compiler(object):
    compiler = None
    os_system = None

    _configurations = ['arch', 'build_type', 'version', ]

    @property
    def arch(self):
        return get_env("CONAN_ARCHS", ["x86", "x86_64"])

    @property
    def build_type(self):
        return get_env("CONAN_BUILD_TYPES", ["Release", "Debug"])

    @property
    def version(self):
        raise NotImplementedError()



@register
class CompilerGCC(Compiler):
    compiler = 'gcc'
    os_system = "Linux"

    @property
    def version(self):
        return get_env("CONAN_GCC_VERSIONS", ["4.9", "5", "6", "7"])


@register
class CompilerClangLinux(Compiler):
    compiler = 'clang'
    os_system = "Linux"

    @property
    def version(self):
        return get_env("CONAN_CLANG_VERSIONS", ["3.8", "3.9", "4.0"])


@register
class CompilerClangApple(Compiler):
    compiler = 'apple-clang'
    os_system = "Darwin"

    @property
    def version(self):
        return get_env("CONAN_APPLE_CLANG_VERSIONS", ["7.3", "8.0", "8.1"])


@register
class CompilerVisualStudio(Compiler):
    compiler = 'Visual Studio'
    os_system = "Windows"
    _configurations = Compiler._configurations + ['runtime', ]

    @property
    def version(self):
        return get_env("CONAN_VISUAL_VERSIONS", ["10", "12", "14"])

    @property
    def runtime(self):
        return get_env("CONAN_VISUAL_RUNTIMES", ["MT", "MD", "MTd", "MDd"])