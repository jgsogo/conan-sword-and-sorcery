# -*- coding: utf-8 -*-

import os

from .base_runner import BaseRunner
from .registry import RunnerRegistry


@RunnerRegistry.register("APPVEYOR")
class AppveyorRunner(BaseRunner):

    def is_pull_request(self):
        return "APPVEYOR_PULL_REQUEST_NUMBER" in os.environ

    def get_branch_name(self):
        return os.getenv("APPVEYOR_REPO_BRANCH")

