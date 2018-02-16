# -*- coding: utf-8 -*-

import os
import logging
from .base_runner import BaseRunner
from .registry import RunnerRegistry
from conan_sword_and_sorcery import __version__

log = logging.getLogger(__name__)


@RunnerRegistry.register("TRAVIS")
class TravisRunner(BaseRunner):

    def __init__(self, compiler, *args, **kwargs):
        super(TravisRunner, self).__init__(compiler=compiler, *args, **kwargs)
        self.use_docker = os.environ.has_key("CONAN_DOCKER_IMAGE") or os.environ.get("CONAN_USE_DOCKER", False)
        if self.use_docker:
            self.docker_image = os.environ.get("CONAN_DOCKER_IMAGE", None)
            log.info("TravisRunner will use docker image '{}'".format(self.docker_image))

            # Impostor for compiler.cmd method
            compiler_cmd = compiler.cmd
            def run_in_docker(command_plain):
                compiler_cmd('docker run {} /bin/sh -c "{}"'.format(self.docker_image, command_plain))
            compiler.cmd = run_in_docker

            os.system("docker pull {}".format(self.docker_image))
            run_in_docker("sudo pip install conan --upgrade")
            run_in_docker("sudo pip install conan_sword_and_sorcery=={} --upgrade".format(__version__))
            run_in_docker("conan user")



