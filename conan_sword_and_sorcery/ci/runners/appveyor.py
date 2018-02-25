# -*- coding: utf-8 -*-

import os

from .base_runner import BaseRunner
from .registry import RunnerRegistry
from conan_sword_and_sorcery.job_generators import JobGeneratorEnviron


@RunnerRegistry.register("APPVEYOR")
class AppveyorRunner(BaseRunner):
    job_generator_class = JobGeneratorEnviron

    def is_pull_request(self):
        return "APPVEYOR_PULL_REQUEST_NUMBER" in os.environ

    def get_branch_name(self):
        return os.getenv("APPVEYOR_REPO_BRANCH")

