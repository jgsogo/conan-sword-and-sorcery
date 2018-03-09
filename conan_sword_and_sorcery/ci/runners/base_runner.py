# -*- coding: utf-8 -*-

import logging
import os
import re

from conan_sword_and_sorcery.utils.cmd import cmd
from conan_sword_and_sorcery.uploader import upload
from conan_sword_and_sorcery.parsers.conanfile import ConanFileWrapper
from conan_sword_and_sorcery.parsers.settings import Settings
from conans.util.env_reader import get_env

log = logging.getLogger(__name__)

SUCCESS = "OK"
FAIL = "FAIL"
DRY_RUN = "DRY_RUN"

STABLE_BRANCH_PATTERN = "^stable\/v?(\d+!)?(\d+)?(\.\d+)*([\.\-\_])?((a(lpha)?|b(eta)?|c|r(c|ev)?|pre(view)?)\d*)?(\.?(post|dev)\d*)?$"


class BaseRunner(object):
    profile = None
    compiler = None
    job_generator_class = None

    def __init__(self, conanfile, settings, osys, dry_run=False):  # type: (str, Settings, str, bool) -> None
        self.conanfile = conanfile
        self.recipe = ConanFileWrapper.parse(conanfile)
        self.job_generator = self.job_generator_class(conanfile_wrapper=self.recipe, settings=settings, osys=osys)
        self.dry_run = dry_run

    def enumerate_jobs(self):
        return self.job_generator.enumerate_jobs()

    def set_compiler(self, compiler):
        self.compiler = compiler
        self.compiler.cmd = self.cmd  # TODO: There is a better way, for sure :S

    def set_profile(self, profile):
        self.profile = profile

    def run(self, options, username, channel):
        conan_ref = "{}/{}".format(username, channel)
        command = ['conan', 'create', self.conanfile, conan_ref,
                   '--profile', self.profile,
                   '--build={}'.format(self.recipe.name),  # Always build this recipe.
                   '--build=outdated']  # TODO: Use a policy for --build?
        build_packages = get_env("CONAN_BUILD_PACKAGES", [])
        for pck in build_packages:
            command += ['--build={}'.format(pck)]
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

    def is_stable_branch(self):
        stable_branch_pattern = os.getenv("CONAN_STABLE_BRANCH_PATTERN", STABLE_BRANCH_PATTERN)
        return re.match(stable_branch_pattern, self.get_branch_name())

    def is_upload_requested(self):
        upload_only_when_stable = os.getenv("CONAN_UPLOAD_ONLY_WHEN_STABLE", False)
        return not upload_only_when_stable or self.is_stable_branch()

    def upload(self, username, channel):
        if self.is_upload_requested():
            upload(recipe=self.recipe, username=username, channel=channel, dry_run=self.dry_run)
        else:
            log.info("Upload not requested for this branch")
