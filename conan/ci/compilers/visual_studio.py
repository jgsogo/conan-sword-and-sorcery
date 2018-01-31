# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env

from .registry import CompilerRegistry
from conan.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    archs=get_env("CONAN_ARCHS", ["x86", "x86_64"]),
    build_types=get_env("CONAN_BUILD_TYPES", ["Release", "Debug"]),
    versions=get_env("CONAN_VISUAL_VERSIONS", ["8", "9", "10", "11", "12", "14", "15"]),
    runtimes=get_env("CONAN_VISUAL_RUNTIMES", ["MT", "MD", "MTd", "MDd"])
    # TODO: Add toolset
)
class CompilerVisualStudio(BaseCompiler):
    def __init__(self, **kwargs):
        super(CompilerVisualStudio, self).__init__(name='visual_studio', **kwargs)
