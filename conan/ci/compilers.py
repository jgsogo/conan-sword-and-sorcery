# -*- coding: utf-8 -*-

from collections import defaultdict
from conans.util.env_reader import get_env


class Compiler(object):
    compiler = None
    _configurations = ['build_types', 'versions', ]

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