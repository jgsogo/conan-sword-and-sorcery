# -*- coding: utf-8 -*-

import unittest
import configparser
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.compilers.visual_studio import CompilerVisualStudio
from conan_sword_and_sorcery.parsers.profile import profile_for, parse_profile
from tests.test_ci.test_compilers.helpers import CompilerMixinTestCase



def mocked_vcvars(mock_sets=None, arch=None, compiler_version=None, check=True):
    if check:
        assert arch == 'x86_64'
        assert compiler_version == '15'
        assert mock_sets.arch == 'x86_64'
        assert mock_sets.compiler.version == '15'
        assert mock_sets.get_safe('os') == 'Windows'
        assert mock_sets.get_safe('invalid') == None
    return "mocked"


class TestCompilerVisualStudio(CompilerMixinTestCase, unittest.TestCase):
    compiler_class = CompilerVisualStudio

    def get_compiler_init_arguments(self):
        return {
            'version': '15',
            'runtime': 'MT',
            'arch': 'x86_64',
            'build_type': 'Release'
        }

    def get_profile_file(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config['settings'] = {'os': 'Windows',
                              'arch': 'x86_64',
                              'build_type': 'Release',
                              'compiler': 'Visual Studio',
                              'compiler.version': '15',
                              'compiler.runtime': 'MT'
                              }
        config['env'] = {}
        return config

    @mock.patch('os.system')
    @mock.patch('conan_sword_and_sorcery.ci.compilers.visual_studio.vcvars_command', side_effect=mocked_vcvars)
    def test_vcvars(self, os_system, _):
        mycommand = "mycommand"

        # TODO: Mock os.system instead of substituting call
        def mycmd(command):
            self.assertEqual("{} && {}".format(mocked_vcvars(check=False), mycommand), command)

        compiler = self.compiler_class(**self.get_compiler_init_arguments())
        compiler.cmd = mycmd
        compiler.run(mycommand)


if __name__ == '__main__':
    unittest.main()
