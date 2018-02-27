# -*- coding: utf-8 -*-

from .base_runner import BaseRunner
from .registry import RunnerRegistry
from conan_sword_and_sorcery.job_generators import JobGeneratorProfiles


@RunnerRegistry.fallback
class ProfilesRunner(BaseRunner):
    job_generator_class = JobGeneratorProfiles

    def get_branch_name(self):
        # TODO: Get from git/hg/svn? Rename this class to 'local' or 'desktop'
        return "testing"
