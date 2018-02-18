# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from conan_sword_and_sorcery.ci.compilers.visual_studio import CompilerVisualStudio
from conan_sword_and_sorcery.profile import profile_for, parse_profile


def mocked_vcvars(mock_sets=None, arch=None, compiler_version=None, check=True):
    if check:
        assert arch == 'x86_64'
        assert compiler_version == '15'
        assert mock_sets.arch == 'x86_64'
        assert mock_sets.compiler.version == '15'
        assert mock_sets.get_safe('os') == 'Windows'
        assert mock_sets.get_safe('invalid') == None
    return "mocked"


class TestCompilerVisualStudio(unittest.TestCase):

    def setUp(self):
        self.version = '15'
        self.runtime = 'MT'
        self.arch = 'x86_64'
        self.build_type = 'Release'
        self.compiler = CompilerVisualStudio(arch=self.arch, build_type=self.build_type,
                                             version=self.version, runtime=self.runtime)

    def test_profile_file(self):
        with profile_for(self.compiler) as ff:
            matches = parse_profile(ff)
            self.assertDictEqual(matches, {'arch': self.arch,
                                           'build_type': self.build_type,
                                           'compiler': self.compiler.id,
                                           'compiler.version': self.version,
                                           'compiler.runtime': self.runtime})

    @mock.patch('os.system')
    @mock.patch('conan_sword_and_sorcery.ci.compilers.visual_studio.vcvars_command', side_effect=mocked_vcvars)
    def test_vcvars(self, os_system, _):
        mycommand = "mycommand"

        # TODO: Mock os.system instead of substituting call
        def mycmd(command):
            self.assertEqual("{} && {}".format(mocked_vcvars(check=False), mycommand), command)

        self.compiler.cmd = mycmd
        self.compiler.run(mycommand)


if __name__ == '__main__':
    unittest.main()
