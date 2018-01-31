# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env

from .registry import CompilerRegistry
from conan.ci.compilers.base_compiler import BaseCompiler


@CompilerRegistry.register(
    arch=["x86", "x86_64"],
    build_type=["Release", "Debug"],
    version=["12", "14", "15"],
    runtime=["MT", "MD", "MTd", "MDd"],
    # TODO: Add toolset
)
class CompilerVisualStudio(BaseCompiler):
    id = 'Visual Studio'
    osys = "Windows"

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