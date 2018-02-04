# -*- coding: utf-8 -*-


from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler


class NoCompiler(BaseCompiler):  # TODO: Refactor to 'HeaderOnlyCompiler'
    id = 'no-compiler'

    @classmethod
    def environment_filters(cls):
        return {}

