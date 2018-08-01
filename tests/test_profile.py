# -*- coding: utf-8 -*-

import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler
from conan_sword_and_sorcery.parsers.profile import profile_for, parse_profile
from conan_sword_and_sorcery.ci.compilers.clang import CompilerClangLinux


class ATestCompiler(BaseCompiler):
    id = 'test_compiler'
    osys = 'test_os'
    arch = 'x86'
    build_type = 'Debug'
    version = '42'

    @property
    def compiler(self):  # This is a convenience function just to pass tests
        return self.id

    def __getattr__(self, item):
        if item == 'compiler.version':    # This is a convenience function just to pass tests
            return self.version
        return super(ATestCompiler, self).__getattr__(item)


class TestProfile(unittest.TestCase):
    def test_profile_file(self):
        compiler = ATestCompiler()
        with profile_for(compiler) as ff:
            profile = parse_profile(ff)
            self.assertEqual(profile['settings']['build_type'], compiler.build_type)
            self.assertEqual(profile['settings']['arch'], compiler.arch)
            self.assertEqual(profile['settings']['compiler'], compiler.id)
            self.assertEqual(profile['settings']['compiler.version'], compiler.version)
            self.assertEqual(profile['settings']['os'], compiler.osys)

    def test_compiler_clang(self):
        version = '3.9'
        libcxx = 'libstdc++11'
        arch = 'x86'
        build_type = 'Release'

        compiler = CompilerClangLinux(arch=arch, build_type=build_type, version=version, libcxx=libcxx)
        with profile_for(compiler) as ff:
            parser = parse_profile(ff)
            options = {}
            for section in parser.sections():
                options.update(parser.items(section))

        self.assertDictEqual(options, {'os': compiler.osys,
                                       'arch': arch,
                                       'build_type': build_type,
                                       'compiler': compiler.id,
                                       'compiler.version': version,
                                       'compiler.libcxx': libcxx,
                                       'CC': '/usr/bin/clang-{}'.format(version),
                                       'CXX': '/usr/bin/clang++-{}'.format(version),})


if __name__ == '__main__':
    unittest.main()
