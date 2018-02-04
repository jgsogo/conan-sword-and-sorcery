# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["3.9", "4.0", "5.0"],
    libcxx=["libstdc++", "libstdc++11", "libc++", ]
)
class CompilerClangLinux(BaseCompiler):
    id = 'clang'
    osys = 'Linux'

    @classmethod
    def environment_filters(cls):
        clang_versions = get_env("CONAN_CLANG_VERSIONS", [])
        if len(clang_versions):
            return {'version': [(cls.id, v) for v in clang_versions]}
        else: return {}


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["7.3", "8.1", "9.0"],
    libcxx=["libstdc++", "libc++", ]
)
class CompilerClangApple(BaseCompiler):
    id = 'apple-clang'
    osys = 'Macos'

    @classmethod
    def environment_filters(cls):
        apple_clang_versions = get_env("CONAN_APPLE_CLANG_VERSIONS", [])
        if len(apple_clang_versions):
            return {'version': [(cls.id, v) for v in apple_clang_versions]}
        else: return {}
