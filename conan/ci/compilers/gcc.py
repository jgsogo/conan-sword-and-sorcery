# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env

from .registry import CompilerRegistry
from conan.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    archs=get_env("CONAN_ARCHS", ["x86", "x86_64"]),
    build_types=get_env("CONAN_BUILD_TYPES", ["Release", "Debug"]),
    versions=get_env("CONAN_GCC_VERSIONS", ["4.9", "5", "6", "7"])
    # TODO: Add libcxx
)
class CompilerGCC(BaseCompiler):
    def __init__(self, **kwargs):
        super(CompilerGCC, self).__init__(name='gcc', **kwargs)
