# -*- coding: utf-8 -*-

import unittest
import re
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.compilers.base_compiler import BaseCompiler
from conan_sword_and_sorcery.profile import profile_for


class ATestCompiler(BaseCompiler):
    id = 'test_compiler'
    osys = 'test_os'
    arch = 'x86'
    build_type = 'Debug'

    @property
    def compiler(self):  # This is a convenience function just to pass tests
        return self.id


class TestProfile(unittest.TestCase):

    def test_profile_file(self):
        eq = re.compile("^(\w+)=([\w_]+)")
        compiler = ATestCompiler()
        matches = 0
        with profile_for(compiler) as ff:
            with open(ff) as f:
                for line in f.readlines():
                    m = eq.match(line)
                    if m:
                        matches += 1
                        self.assertEqual(getattr(compiler, m.group(1)), m.group(2))
        self.assertEqual(matches, 3)

if __name__ == '__main__':
    unittest.main()
