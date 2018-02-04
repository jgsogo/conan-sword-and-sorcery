# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["4.9", "5", "6", "7"],
    libcxx=["libstdc++", "libstdc++11", ]
)
class CompilerGCC(BaseCompiler):
    id = 'gcc'
    osys = 'Linux'

    def __str__(self):
        return "{} {} ({}) {} {}".format(self.id, self.version, self.arch, self.build_type, self.libcxx)

    @classmethod
    def environment_filters(cls):
        gcc_versions = get_env("CONAN_GCC_VERSIONS", [])
        if len(gcc_versions):
            return {'version': [(cls.id, v) for v in gcc_versions]}
        else: return {}
