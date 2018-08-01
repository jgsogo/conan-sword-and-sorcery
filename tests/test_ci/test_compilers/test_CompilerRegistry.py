# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.compilers import CompilerRegistry
from tests.utils import TestCaseEnvClean, count_registered_compilers
from conan_sword_and_sorcery.utils.environ import context_env


class TestCompilerRegistry(TestCaseEnvClean):

    def setUp(self):
        self.registry = CompilerRegistry()
        self.os = ["Windows", "Linux", "Macos",]

    def test_base(self):
        self.assertEqual(len(list(self.registry.get_compilers(os=self.os))),
                         count_registered_compilers(osys=self.os))
        self.assertEqual(len(list(self.registry.get_compilers(os=self.os, arch=['x86', ]))),
                         count_registered_compilers(osys=self.os, arch=['x86', ]))
        self.assertEqual(len(list(self.registry.get_compilers(os=self.os, arch=['x86', ], version=[("gcc", "7"), ]))),
                         count_registered_compilers(os=self.os, arch=['x86'], id='gcc', version='7')
                         )
        self.assertEqual(len(list(self.registry.get_compilers(os=self.os, arch=['x86', ], version=[("gcc", "7"), ("Visual Studio", "12"), ]))),
                         count_registered_compilers(os=self.os, arch=['x86'], id=['gcc', 'Visual Studio'], version=['7', '12', ])
                         )

    def test_invalid_argument(self):
        self.assertEqual(len(list(self.registry.get_compilers(os=self.os, invalid_arg=["x86", ]))),
                         count_registered_compilers(osys=self.os, ))  # TODO: It may be invalid for some, but valid for others, so do not discard compilers if you pass them strange arguments

    def test_invalid_value(self):
        self.assertEqual(len(list(self.registry.get_compilers(os=self.os, arch=["x86000", ]))), 0)


class TestCompilerRegistryEnvironmentFilters(TestCaseEnvClean):
    def setUp(self):
        self.registry = CompilerRegistry()

    def test_one_compiler(self):
        with context_env(CONAN_VISUAL_VERSIONS='10'):
            self.assertDictEqual(self.registry.environment_filters(),
                                 {'version': {('Visual Studio', '10'),
                                              }})

        with context_env(CONAN_VISUAL_VERSIONS='10,12'):
            self.assertDictEqual(self.registry.environment_filters(),
                                 {'version': {('Visual Studio', '10'),
                                              ('Visual Studio', '12')
                                              }})

    def test_several_compilers(self):
        with context_env(CONAN_VISUAL_VERSIONS='10', CONAN_GCC_VERSIONS='3,4'):
            self.assertDictEqual(self.registry.environment_filters(),
                                 {'version': {('gcc', '3'),
                                              ('gcc', '4'),
                                              ('Visual Studio', '10')
                                              }})

    def test_several_filters(self):
        with context_env(CONAN_VISUAL_VERSIONS='10', CONAN_VISUAL_RUNTIMES='MT,MTd'):
            self.assertDictEqual(self.registry.environment_filters(),
                                 {'version': {('Visual Studio', '10')
                                              },
                                  'runtime': {"MT", "MTd"},})


if __name__ == '__main__':
    unittest.main()
