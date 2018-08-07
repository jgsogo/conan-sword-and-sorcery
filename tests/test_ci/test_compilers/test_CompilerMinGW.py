# -*- coding: utf-8 -*-

import unittest
import configparser
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.compilers.mingw import CompilerMinGW
from tests.test_ci.test_compilers.helpers import CompilerMixinTestCase


class TestCompilerMinGW(CompilerMixinTestCase, unittest.TestCase):
    compiler_class = CompilerMinGW

    def get_compiler_init_arguments(self):
        return {
            'version': '4.9',
            'arch': 'x86',
            'build_type': 'Release',
            'exception': 'seh',
            'threads': 'posix',
        }

    def get_profile_file(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config['settings'] = {'os': 'Windows',
                              'arch': 'x86',
                              'build_type': 'Release',
                              'compiler': 'gcc',
                              'compiler.version': '4.9',
                              'compiler.exception': 'seh',
                              'compiler.threads': 'posix',
                              'os_build': 'Windows',
                              'arch_build': 'x86',
                              }
        config['env'] = {}
        config['build_requires'] = {'mingw_installer/1.0@conan/stable': '',
                                    'msys2_installer/latest@bincrafters/stable': ''}
        return config


if __name__ == '__main__':
    unittest.main()
