# -*- coding: utf-8 -*-

import platform
import itertools
from collections import defaultdict
from conans.util.env_reader import get_env


class OperatingSystem(object):
    os = platform.system()

    @property
    def archs(self):
        return get_env("CONAN_ARCHS", ["x86", "x86_64"])


class Compiler(object):
    compiler = None
    _configurations = ['compiler', 'build_types', 'versions', ]

    @property
    def build_types(self):
        return get_env("CONAN_BUILD_TYPES", ["Release", "Debug"])

    @property
    def versions(self):
        raise NotImplementedError()

    # Add a factory
    _registry = defaultdict(list)

    @classmethod
    def register(cls, compiler):
        cls._registry[compiler.os_system].append(compiler)
        return compiler


@Compiler.register
class CompilerGCC(Compiler):
    compiler = 'gcc'
    os_system = "Linux"

    @property
    def versions(self):
        return get_env("CONAN_GCC_VERSIONS", ["4.9", "5", "6", "7"])


@Compiler.register
class CompilerClangLinux(Compiler):
    compiler = 'clang'
    os_system = "Linux"

    @property
    def versions(self):
        return get_env("CONAN_CLANG_VERSIONS", ["3.8", "3.9", "4.0"])


@Compiler.register
class CompilerClangApple(Compiler):
    compiler = 'apple-clang'
    os_system = "Darwin"

    @property
    def versions(self):
        return get_env("CONAN_APPLE_CLANG_VERSIONS", ["7.3", "8.0", "8.1"])


@Compiler.register
class CompilerVisualStudio(Compiler):
    compiler = 'Visual Studio'
    os_system = "Windows"
    _configurations = Compiler._configurations + ['runtimes', ]

    @property
    def versions(self):
        return get_env("CONAN_VISUAL_VERSIONS", ["10", "12", "14"])

    @property
    def runtimes(self):
        return get_env("CONAN_VISUAL_RUNTIMES", ["MT", "MD", "MTd", "MDd"])


def get_settings(os_system=OperatingSystem()):
    compiler_classes = Compiler._registry[os_system.os]
    configurations = list(set(c._configurations for c in compiler_classes))

    cross_configs = []
    for compiler in compiler_classes:
        r = [compiler, ] + [getattr(compiler, config, []) for config in configurations]
        cross_configs.append(itertools.product(*r))

    for cross_config in cross_configs:
        compiler = cross_config[0]()
        yield os_system, compiler, {key: value for key, value in zip(configurations, cross_config[1:])}
