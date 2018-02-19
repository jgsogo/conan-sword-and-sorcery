# -*- coding: utf-8 -*-

import logging
import uuid

from conan_sword_and_sorcery.utils.cmd import cmd

log = logging.getLogger(__name__)

SUCCESS = "OK"
FAIL = "FAIL"
DRY_RUN = "DRY_RUN"


class BaseRunner(object):
    profile = None

    def __init__(self, conanfile, recipe, dry_run=False):
        self.conanfile = conanfile
        self.recipe = recipe
        self.dry_run = dry_run

    def set_compiler(self, compiler):
        self.compiler = compiler
        self.compiler.cmd = self.cmd  # TODO: There is a better way, for sure :S

    def set_profile(self, profile):
        self.profile = profile

    def run(self, options, username, channel):
        conan_ref = "{}/{}".format(username, channel)
        command = ['conan', 'create', self.conanfile, conan_ref,
                   '--profile', self.profile, '--build=missing']
        for k, v in options.items():
            command += ['-o', '{}:{}={}'.format(self.recipe.name, k, v)]
        return self.compiler.run(' '.join(command))

    def cmd(self, command):
        log.info("command to run: {}".format(command))
        if not self.dry_run:
            ret = cmd(command, exception=None)
            return SUCCESS if ret == 0 else FAIL
        return DRY_RUN
