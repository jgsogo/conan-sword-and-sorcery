# -*- coding: utf-8 -*-

import logging
import os

from .base_runner import BaseRunner
from .registry import RunnerRegistry
from ._docker import DockerMixin

log = logging.getLogger(__name__)


@RunnerRegistry.register("TRAVIS")
class TravisRunner(DockerMixin, BaseRunner):

    def is_pull_request(self):
        return os.getenv("TRAVIS_PULL_REQUEST") != "false"

    def get_branch_name(self):
        return os.getenv("TRAVIS_BRANCH")
