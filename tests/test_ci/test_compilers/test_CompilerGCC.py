# -*- coding: utf-8 -*-

import unittest
import configparser
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.compilers.gcc import CompilerGCC
from tests.test_ci.test_compilers.helpers import CompilerMixinTestCase


class TestCompilerGCC(CompilerMixinTestCase, unittest.TestCase):
    compiler_class = CompilerGCC

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
                              'compiler': 'gcc',
                              'compiler.version': '4.9',
                              'compiler.libcxx': 'libstdc++11',
                              }
        config['env'] = {'CC': '/usr/bin/gcc-4.9',
                         'CXX': '/usr/bin/g++-4.9', }
        return config


if __name__ == '__main__':
    unittest.main()
