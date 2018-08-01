# -*- coding: utf-8 -*-

import unittest
import configparser
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.compilers.clang import CompilerClangApple
from tests.test_ci.test_compilers.helpers import CompilerMixinTestCase


class TestCompilerClangApple(CompilerMixinTestCase, unittest.TestCase):
    compiler_class = CompilerClangApple

    def get_compiler_init_arguments(self):
        return {
            'version': '4.9',
            'arch': 'x86',
            'build_type': 'Release',
            'libcxx': 'libstdc++11',
        }

    def get_profile_file(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config['settings'] = {'os': 'Macos',
                              'arch': 'x86',
                              'build_type': 'Release',
                              'compiler': 'apple-clang',
                              'compiler.version': '4.9',
                              'compiler.libcxx': 'libstdc++11',
                              }
        config['env'] = {'CC': '/usr/bin/clang',
                         'CXX': '/usr/bin/clang++', }
        return config


if __name__ == '__main__':
    unittest.main()
