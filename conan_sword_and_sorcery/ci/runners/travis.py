# -*- coding: utf-8 -*-

import os
import logging
from .base_runner import BaseRunner
from .registry import RunnerRegistry
from conan_sword_and_sorcery import __version__

log = logging.getLogger(__name__)


@RunnerRegistry.register("TRAVIS")
class TravisRunner(BaseRunner):
    docker_conan_project_dirname = "/home/conan/project"

    def __init__(self, *args, **kwargs):
        super(TravisRunner, self).__init__(*args, **kwargs)
        self.use_docker = ("CONAN_DOCKER_IMAGE" in os.environ) or (os.environ.get("CONAN_USE_DOCKER", False))
        if self.use_docker:
            self.docker_image = os.environ.get("CONAN_DOCKER_IMAGE", None)
            log.info("TravisRunner will use docker image '{}'".format(self.docker_image))
            os.system("docker pull {}".format(self.docker_image))
            self._run_in_docker('sudo pip install -U conan conan_sword_and_sorcery=={} && conan user'.format(__version__))

    def set_profile(self, profile):
        super(TravisRunner, self).set_profile(profile)
        command = 'docker cp {profile} {image}:{profile}'.format(
            image=self.docker_image,
            profile=profile,
        )
        super(TravisRunner, self).cmd(command)

    def _run_in_docker(self, command):
        docker_command = 'docker run --rm -v {cwd}:{docker_dirname} {image} /bin/sh -c "{command}"'.format(
            cwd=os.getcwd(),
            image=self.docker_image,
            command=command,
            docker_dirname=self.docker_conan_project_dirname,
        )
        return super(TravisRunner, self).cmd(docker_command)

    def cmd(self, command):
        if not self.use_docker:
            return super(TravisRunner, self).cmd(command)
        else:
            command = command.replace(os.getcwd(), self.docker_conan_project_dirname)  # TODO: Make a better approach
            return self._run_in_docker(command)



