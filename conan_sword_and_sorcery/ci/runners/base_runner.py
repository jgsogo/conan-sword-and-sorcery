# -*- coding: utf-8 -*-

import logging
import sys

log = logging.getLogger(__name__)


class BaseRunner(object):
    profile = None
    conanfile = None
    recipe = None

    def __init__(self, compiler):
        self.compiler = compiler

    def run(self, options, dry_run=False):
        log.debug("Profile file: {}\n".format(self.profile))

        # TODO: Code to get user/channel

        command = ['conan', 'create', self.conanfile, 'jgsogo/testing',
                   '--profile', self.profile, '--build=missing']
        for k, v in options.items():
            command += ['-o', '{}:{}={}'.format(self.recipe.name, k, v)]
        return self.compiler.run(command, dry_run=dry_run)
