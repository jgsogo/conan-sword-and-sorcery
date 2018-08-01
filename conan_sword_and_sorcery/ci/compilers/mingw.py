# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["4.9", "5", "6", "7"],
    exception=["seh", ],
    thread=["posix", "win32", ]
)
class CompilerMinGW(BaseCompiler):
    id = 'gcc'
    osys = 'Windows'

    def __init__(self, arch, *args, **kwargs):
        super(CompilerMinGW, self).__init__(arch=arch, *args, **kwargs)
        self.arch_build = arch  # TODO: Move this to base compiler class (or inherit profile from defaults).

    def __str__(self):
        return "MinGW/{} {} ({}) {} {} {}".format(self.id, self.version, self.arch, self.build_type, self.exception, self.thread)

    def update_settings(self, settings):
        super(CompilerMinGW, self).update_settings(settings)

    @classmethod
    def environment_filters(cls):
        # TODO: Here we need to parse MINGW_CONFIGURATIONS with all the information.
        mingw_versions = get_env("CONAN_MINGW_VERSIONS", [])
        mingw_exceptions = get_env("CONAN_MINGW_EXCEPTIONS", [])
        mingw_threads = get_env("CONAN_MINGW_THREADS", [])
        r = {}
        if len(mingw_versions):
            r['version'] = [(cls.id, v) for v in mingw_versions]
        if len(mingw_exceptions):
            r['exception'] = mingw_exceptions
        if len(mingw_threads):
            r['thread'] = mingw_threads
        return r

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
