# -*- coding: utf-8 -*-

from .registry import CompilerRegistry
from conan.ci.compilers.base_compiler import BaseCompiler


class NoCompiler(BaseCompiler):
    id = 'no-compiler'
    VERSION = 'no-version'

    @classmethod
    def environment_filters(cls):
        return {'version': [(cls.id, cls.VERSION),]}


@CompilerRegistry.register(version=[NoCompiler.VERSION, ])
class NoCompilerWindows(NoCompiler):
    osys = "Windows"


@CompilerRegistry.register(version=[NoCompiler.VERSION, ])
class NoCompilerLinux(NoCompiler):
    osys = "Linux"


@CompilerRegistry.register(version=[NoCompiler.VERSION, ])
class NoCompilerMacos(NoCompiler):
    osys = "Macos"
