# -*- coding: utf-8 -*-

import unittest
import configparser
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.compilers.clang import CompilerClangLinux
from tests.test_ci.test_compilers.helpers import CompilerMixinTestCase


class TestCompilerClangLinux(CompilerMixinTestCase, unittest.TestCase):
    compiler_class = CompilerClangLinux

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
        config['settings'] = {'os': 'Linux',
                              'arch': 'x86',
                              'build_type': 'Release',
                              'compiler': 'clang',
                              'compiler.version': '4.9',
                              'compiler.libcxx': 'libstdc++11',
                              }
        config['env'] = {'CC': '/usr/bin/clang-4.9',
                         'CXX': '/usr/bin/clang++-4.9', }
        return config


if __name__ == '__main__':
    unittest.main()
