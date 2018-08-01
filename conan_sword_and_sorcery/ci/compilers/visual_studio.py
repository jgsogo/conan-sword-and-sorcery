# -*- coding: utf-8 -*-

import logging
from collections import namedtuple

from conans.util.env_reader import get_env
from conans.tools import vcvars_command

from .registry import CompilerRegistry
from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler

log = logging.getLogger(__name__)


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["11", "12", "14", "15"],
    runtime=["MT", "MD", "MTd", "MDd"],
    # TODO: Add toolset
)
class CompilerVisualStudio(BaseCompiler):
    id = 'Visual Studio'
    osys = "Windows"

    def __str__(self):
        return "{} {} ({}) {} {}".format(self.id, self.version, self.arch, self.build_type, self.runtime)

    @classmethod
    def validate(cls, build_type, runtime, **kwargs):
        if super(CompilerVisualStudio, cls).validate(build_type=build_type, runtime=runtime, **kwargs):
            return (build_type == "Debug" and runtime.endswith('d')) or \
                   (build_type == "Release" and not runtime.endswith('d'))
        else:
            return False

    def update_settings(self, settings):
        super(CompilerVisualStudio, self).update_settings(settings)
        if 'runtime' in settings.compiler._data.keys():
            settings.compiler.runtime = self.runtime

    def populate_profile(self, configfile):
        super(CompilerVisualStudio, self).populate_profile(configfile)
        configfile['settings']['compiler.runtime'] = self.runtime

    @classmethod
    def environment_filters(cls):
        visual_versions = get_env("CONAN_VISUAL_VERSIONS", [])
        visual_runtimes = get_env("CONAN_VISUAL_RUNTIMES", [])
        r = {}
        if len(visual_versions):
            r['version'] = [(cls.id, v) for v in visual_versions]
        if len(visual_runtimes):
            r['runtime'] = visual_runtimes
        return r

    def run(self, command_plain):
        log.debug("CompilerVisualStudio::run")

        # Need to call vcvars before compiler
        def get_safe(x):
            if x == 'os':
                return self.osys
            log.error("CompilerVisualStudio requested '{}' from setting, but it is not available.".format(x))
            return None
        compiler_set = namedtuple("compiler", "version")(self.version)
        mock_sets = namedtuple("mock_settings",
                               ["arch", "compiler", "get_safe", ])(self.arch, compiler_set,
                                                         lambda x: get_safe(x))
        pre_command = vcvars_command(mock_sets, arch=self.arch, compiler_version=self.version)

        command = "{} && {}".format(pre_command, command_plain)
        return super(CompilerVisualStudio, self).run(command)
