# -*- coding: utf-8 -*-

import sys


class BaseRunner(object):
    profile = None

    def __init__(self, compiler):
        self.compiler = compiler

    def set_profile_file(self, filename):
        self.profile = filename

    def run(self, options):
        sys.stdout.write("Profile file: {}\n".format(self.profile))
        with open(self.profile, 'r') as f:
            for line in f.readlines():
                sys.stdout.write("\t> {}".format(line))
        sys.stdout.write("Options:\n")
        for k, v in options.items():
            sys.stdout.write("\t> {:<14}= {}\n".format(k, v))
