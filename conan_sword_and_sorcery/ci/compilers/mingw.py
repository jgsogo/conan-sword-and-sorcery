# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["4.9", "5", "6", "7"],
)
class CompilerMinGW(BaseCompiler):
    id = 'gcc'
    osys = 'Windows'

    def __init__(self, arch, *args, **kwargs):
        super(CompilerMinGW, self).__init__(arch=arch, *args, **kwargs)
        self.arch_build = arch  # TODO: Move this to base compiler class (or inherit profile from defaults).

    def __str__(self):
        return "MinGW/{} {} ({}) {}".format(self.id, self.version, self.arch, self.build_type)

    def update_settings(self, settings):
        super(CompilerMinGW, self).update_settings(settings)

    @classmethod
    def environment_filters(cls):
        # TODO: Here we need to parse: MINGW_CONFIGURATIONS with all the information.
        gcc_versions = get_env("CONAN_MINGW_VERSIONS", [])
        if len(gcc_versions):
            return {'version': [(cls.id, v) for v in gcc_versions]}
        else: return {}

    def populate_profile_settings(self, f):
        super(CompilerMinGW, self).populate_profile_settings(f)
        f.write("compiler.exception=seh\n")
        f.write("compiler.libcxx=libstdc++11\n")
        f.write("compiler.threads=posix\n")
        f.write("os_build={}\n".format(self.osys))
        f.write("arch_build={}\n".format(self.arch_build))

        f.write("\n")
        f.write("[build_requires]\n")
        f.write("mingw_installer/1.0@conan/stable\n")
        f.write("msys2_installer/latest@bincrafters/stable\n")

    def populate_profile_env(self, f):
        super(CompilerMinGW, self).populate_profile_env(f)
        # f.write("CC=/usr/bin/gcc-{}\n".format(self.version))
        # f.write("CXX=/usr/bin/g++-{}\n".format(self.version))
