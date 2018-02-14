# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from conans.tools import vcvars_command


class BaseRunner(object):
    profile = None
    conanfile = None
    recipe = None

    def __init__(self, compiler):
        self.compiler = compiler

    def run(self, options):
        sys.stdout.write("Profile file: {}\n".format(self.profile))
        with open(self.profile, 'r') as f:
            for line in f.readlines():
                sys.stdout.write("\t> {}".format(line))
        sys.stdout.write("Options:\n")
        for k, v in options.items():
            sys.stdout.write("\t> {:<14}= {}\n".format(k, v))

        # TODO: Code to get user/channel

        command = ['conan', 'create', self.conanfile, 'jgsogo/testing',
                   '--profile', self.profile, '--build=missing']
        for k, v in options.items():
            command += ['-o', '{}:{}={}'.format(self.recipe.name, k, v)]
        self.compiler.run(command)
        # os.system(' '.join(command))
        """
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        for line in process.stdout:
            sys.stdout.write(str(line))
        """
        # process.returncode
