# -*- coding: utf-8 -*-

import logging
import os
import re

from conan_sword_and_sorcery.utils.cmd import cmd
from conan_sword_and_sorcery.uploader import upload

log = logging.getLogger(__name__)

SUCCESS = "OK"
FAIL = "FAIL"
DRY_RUN = "DRY_RUN"


class BaseRunner(object):
    profile = None
    compiler = None

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
                   '--profile', self.profile, '--build=missing']  # TODO: Use a policy for --build?
        for k, v in options.items():
            command += ['-o', '{}:{}={}'.format(self.recipe.name, k, v)]
        return self.compiler.run(' '.join(command))

    def cmd(self, command):
        log.info("command to run: {}".format(command))
        if not self.dry_run:
            ret = cmd(command, exception=None)
            return SUCCESS if ret == 0 else FAIL
        return DRY_RUN

    def is_pull_request(self):
        raise NotImplementedError  # Travis, Appveyor,... will implement it

    def get_branch_name(self):
        raise NotImplementedError  # Travis, Appveyor,... will implement it

    def is_upload_requested(self):
        upload_only_when_stable = os.getenv("CONAN_UPLOAD_ONLY_WHEN_STABLE", False)
        if upload_only_when_stable:
            stable_branch_pattern = os.getenv("CONAN_STABLE_BRANCH_PATTERN", "master")
            return re.match(stable_branch_pattern, self.get_branch_name())
        return True

    def upload(self, username, channel):
        if self.is_upload_requested():
            upload(recipe=self.recipe, username=username, channel=channel, dry_run=self.dry_run)
        else:
            log.info("Upload not requested for this branch")
