# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


class CompilerClangBase(BaseCompiler):
    clang_versions_env_variable = None

    def __str__(self):
        return "{} {} ({}) {} {}".format(self.id, self.version, self.arch, self.build_type, self.libcxx)

    def update_settings(self, settings):
        super(CompilerClangBase, self).update_settings(settings)
        if 'libcxx' in settings.compiler._data.keys():
            settings.compiler.libcxx = self.libcxx

    def populate_profile(self, configfile):
        super(CompilerClangBase, self).populate_profile(configfile)
        configfile['settings']['compiler.libcxx'] = self.libcxx

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

    def populate_profile(self, configfile):
        super(CompilerClangLinux, self).populate_profile(configfile)
        configfile['env']['CC'] = '/usr/bin/clang-{}'.format(self.version)
        configfile['env']['CXX'] = '/usr/bin/clang++-{}'.format(self.version)


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["7.3", "8.1", "9.0", "9.1",],
    libcxx=["libstdc++", "libc++", ]
)
class CompilerClangApple(CompilerClangBase):
    id = 'apple-clang'
    osys = 'Macos'
    clang_versions_env_variable = "CONAN_APPLE_CLANG_VERSIONS"

    def populate_profile(self, configfile):
        super(CompilerClangApple, self).populate_profile(configfile)
        configfile['env']['CC'] = '/usr/bin/clang'.format(self.version)  # TODO: Test it in mac, no version appended?
        configfile['env']['CXX'] = '/usr/bin/clang++'.format(self.version)  # TODO: Test it in mac, no version appended?
