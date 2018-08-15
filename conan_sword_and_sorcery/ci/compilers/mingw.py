# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["4.9", "5", "6", "7"],
    exception=["seh", ],
    threads=["posix", "win32", ]
)
class CompilerMinGW(BaseCompiler):
    id = 'gcc'
    osys = 'Windows'

    def __init__(self, arch, *args, **kwargs):
        super(CompilerMinGW, self).__init__(arch=arch, *args, **kwargs)
        self.arch_build = arch  # TODO: Move this to base compiler class (or inherit profile from defaults).

    def __str__(self):
        return "MinGW/{} {} ({}) {} {} {}".format(self.id, self.version, self.arch, self.build_type, self.exception, self.threads)

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
            r['threads'] = mingw_threads
        return r

    def populate_profile(self, configfile):
        super(CompilerMinGW, self).populate_profile(configfile)
        configfile['settings']['compiler.exception'] = self.exception
        configfile['settings']['compiler.version'] = self.version
        configfile['settings']['compiler.threads'] = self.threads

        configfile['settings']['os_build'] = self.osys
        configfile['settings']['arch_build'] = self.arch_build

        # f.write("compiler.libcxx=libstdc++11\n")

        configfile['build_requires']['mingw_installer/1.0@conan/stable'] = None
        configfile['build_requires']['msys2_installer/latest@bincrafters/stable'] = None

