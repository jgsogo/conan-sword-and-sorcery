# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


class CompilerClangBase(BaseCompiler):
    clang_versions_env_variable = None

    def update_settings(self, settings):
        super(CompilerClangBase, self).update_settings(settings)
        settings.compiler.libcxx = self.libcxx

    def populate_profile_settings(self, f):
        super(CompilerClangBase, self).populate_profile_settings(f)
        f.write("compiler.libcxx={}\n".format(self.libcxx))

    @classmethod
    def environment_filters(cls):
        clang_versions = get_env(cls.clang_versions_env_variable, [])
        if len(clang_versions):
            return {'version': [(cls.id, v) for v in clang_versions]}
        else:
            return {}


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["3.9", "4.0", "5.0"],
    libcxx=["libstdc++", "libstdc++11", "libc++", ]
)
class CompilerClangLinux(CompilerClangBase):
    id = 'clang'
    osys = 'Linux'
    clang_versions_env_variable="CONAN_CLANG_VERSIONS"


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["7.3", "8.1", "9.0"],
    libcxx=["libstdc++", "libc++", ]
)
class CompilerClangApple(CompilerClangBase):
    id = 'apple-clang'
    osys = 'Macos'
    clang_versions_env_variable = "CONAN_APPLE_CLANG_VERSIONS"
