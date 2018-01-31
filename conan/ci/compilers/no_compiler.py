# -*- coding: utf-8 -*-

from .registry import CompilerRegistry
from conan.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(os=["Windows", "Linux", "Macos",])
class NoCompiler(BaseCompiler):
    id = 'no-compiler'

    @classmethod
    def environment_filters(cls):
        return {}