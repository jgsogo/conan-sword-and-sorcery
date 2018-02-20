# -*- coding: utf-8 -*-
import os
import uuid
import logging

from conan_sword_and_sorcery import __version__
from conan_sword_and_sorcery.utils.docker import DockerHelper
from conan_sword_and_sorcery.parsers.conan_conf import ConanConf
from .base_runner import SUCCESS, FAIL, DRY_RUN

log = logging.getLogger(__name__)


def transplant_path(fullpath, ori_rel, tgt_rel):
    return os.path.join(tgt_rel, os.path.relpath(fullpath, ori_rel))


class DockerMixin(object):
    docker_helper = None
    docker_home = "/home/conan"
    docker_project = os.path.join(docker_home, 'project')
    docker_profiles = os.path.join(docker_home, 'profiles')
    docker_storage_path = os.path.join(docker_home, '.conan', 'data')  # TODO: It may be other. We can change it afterwards to point to the mounted path

    def __init__(self, conanfile, *args, **kwargs):
        self.use_docker = ("CONAN_DOCKER_IMAGE" in os.environ) or (os.environ.get("CONAN_USE_DOCKER", False))
        if self.use_docker:
            conanfile = transplant_path(conanfile, os.getcwd(), self.docker_project)
        super(DockerMixin, self).__init__(conanfile=conanfile, *args, **kwargs)

    def set_compiler(self, compiler):
        if self.use_docker:
            docker_image = os.environ.get("CONAN_DOCKER_IMAGE", None)  # TODO: Implement auto-name based on compiler

            if not self.docker_helper or self.docker_helper.image != docker_image:
                # Do not pull again if it is already running
                log.info("TravisRunner will use docker image '{}'".format(docker_image))
                self.docker_helper = DockerHelper(image=docker_image)
                self.docker_helper.pull()

                # Get conan storage/path
                host_conf = ConanConf()
                host_storage = host_conf.get('storage', 'path')

                # Map some directories
                self.docker_helper.add_mount_unit(os.getcwd(), self.docker_project)
                self.docker_helper.add_mount_unit(os.path.expanduser("~"), self.docker_home)  # Required
                self.docker_helper.add_mount_unit(host_storage, self.docker_storage_path)

                # Run the container
                self.docker_helper.run()

                # TODO: Remove this
                try:
                    from conan_sword_and_sorcery.utils.cmd import cmd
                    print("=== HOST ===")
                    cmd("ls -la {}".format(host_storage))
                    cmd("id -u")
                    print("=== DOCKER ===")
                    self.docker_helper.run_in_docker("ls -la {}".format(self.docker_storage_path))
                    self.docker_helper.run_in_docker("id -u")
                except Exception:
                    pass

                # Install what is needed
                self.docker_helper.run_in_docker("pip install -U conan conan_sword_and_sorcery=={version} && conan user".format(version=__version__))

                # Create profiles directory
                self.docker_helper.run_in_docker("mkdir {profile_dir}".format(profile_dir=self.docker_profiles))

        super(DockerMixin, self).set_compiler(compiler)

    def set_profile(self, profile):
        if self.use_docker:
            tgt_name = os.path.join(self.docker_profiles, os.path.basename(profile))
            self.docker_helper.copy(profile, tgt_name)
            profile = tgt_name
        super(DockerMixin, self).set_profile(profile)

    def cmd(self, command):
        if not self.use_docker:
            return super(DockerMixin, self).cmd(command)
        else:
            if not self.dry_run:
                ret = self.docker_helper.run_in_docker(command)
                return SUCCESS if ret == 0 else FAIL
            return DRY_RUN

    def upload(self, username, channel):
        if self.use_docker:
            self.docker_helper.run_in_docker("chmod -R 777 {}".format(self.docker_storage_path))
        super(DockerMixin, self).upload(username, channel)
