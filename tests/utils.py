# -*- coding: utf-8 -*-

import unittest

from conan_sword_and_sorcery.utils.environ import clean_context_env
from conan_sword_and_sorcery.ci.compilers import CompilerRegistry


class TestCaseEnvClean(unittest.TestCase):
    def run(self, *args, **kwargs):
        with clean_context_env(pattern="(CONAN_.*)|(TRAVIS)|(APPVEYOR)"):  # TODO: What else?
            super(TestCaseEnvClean, self).run(*args, **kwargs)


def count_registered_compilers():
    for class_holder in CompilerRegistry._registry:
        for conf in class_holder.explode():
            print(conf._data)