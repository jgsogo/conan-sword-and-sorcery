# -*- coding: utf-8 -*-

import logging
import sys
import os

log = logging.getLogger(__name__)


class BaseRunner(object):
    profile = None

    def __init__(self, compiler, conanfile, recipe, dry_run=False):
        self.compiler = compiler
        self.conanfile = conanfile
        self.recipe = recipe
        self.dry_run = dry_run
        self.compiler.cmd = self.cmd  # TODO: There is a better way, for sure :S

    def set_profile(self, profile):
        self.profile = profile

    def run(self, options):
        log.debug("Profile file: {}\n".format(self.profile))

        # TODO: Code to get user/channel

        command = ['conan', 'create', self.conanfile, 'jgsogo/testing',
                   '--profile', self.profile, '--build=missing']
        for k, v in options.items():
            command += ['-o', '{}:{}={}'.format(self.recipe.name, k, v)]
        return self.compiler.run(' '.join(command))

    def cmd(self, command):
        log.info("command to run: {}".format(command))
        if not self.dry_run:
            ret = os.system(command)  # TODO: May use subprocess
            return "OK" if ret == 0 else "FAIL"
        return "DRY_RUN"
