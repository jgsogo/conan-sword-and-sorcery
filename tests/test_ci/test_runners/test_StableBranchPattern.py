# -*- coding: utf-8 -*-

import re
import os
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


from conan_sword_and_sorcery.ci.runners.base_runner import STABLE_BRANCH_PATTERN


class TestStableBranchPattern(unittest.TestCase):
    # Test cases based on http://legacy.python.org/dev/peps/pep-0440/#final-releases
    version_pre = ""

    def setUp(self):
        self.pattern = re.compile(STABLE_BRANCH_PATTERN)

    def test_final_releases(self):
        self.assertTrue(self.pattern.match("stable/{}0.9".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}0.9.2".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}2.0.1".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}3.3.9.45".format(self.version_pre)))

    def test_date_based(self):
        self.assertTrue(self.pattern.match("stable/{}2012.09".format(self.version_pre)))

    def test_pre_release(self):
        self.assertTrue(self.pattern.match("stable/{}1.2a3".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}1.2alpha3".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}1.2b3".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}1.2beta3".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}3.4rc3".format(self.version_pre)))

    def test_post_release(self):
        self.assertTrue(self.pattern.match("stable/{}1.2.post12".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}1.2a3.post12".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}1.2rc4.post12".format(self.version_pre)))

    def test_developmental_release(self):
        self.assertTrue(self.pattern.match("stable/{}1.2.dev12345".format(self.version_pre)))

        self.assertTrue(self.pattern.match("stable/{}1.2a3.dev12345".format(self.version_pre)))
        self.assertTrue(self.pattern.match("stable/{}1.2rc4.dev12345".format(self.version_pre)))
        # self.assertTrue(self.pattern.match("stable/{}1.2.post12.dev12345".format(self.version_pre)))
        # self.assertTrue(self.pattern.match("stable/{}1.2rc4.post12.dev12345".format(self.version_pre)))

    def test_version_epochs(self):
        self.assertTrue(self.pattern.match("stable/{}3!3.4".format(self.version_pre)))

    def test_false(self):
        self.assertFalse(self.pattern.match("{}1.2.3".format(self.version_pre)))
        self.assertFalse(self.pattern.match("a1.2.3".format(self.version_pre)))
        self.assertFalse(self.pattern.match("{}1.2.dev".format(self.version_pre)))
        self.assertFalse(self.pattern.match("{}1.2.3.beta3".format(self.version_pre)))


class TestStableBranchPatternWithV(TestStableBranchPattern):
    version_pre = "v"



