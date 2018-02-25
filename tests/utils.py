# -*- coding: utf-8 -*-

import unittest

from conan_sword_and_sorcery.utils.environ import clean_context_env


class TestCaseEnvClean(unittest.TestCase):
    def run(self, *args, **kwargs):
        with clean_context_env(pattern="(CONAN_.*)|(TRAVIS)|(APPVEYOR)"):  # TODO: What else?
            super(TestCaseEnvClean, self).run(*args, **kwargs)
