# -*- coding: utf-8 -*-
import os
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

    def __init__(self, conanfile, *args, **kwargs):
        self.use_docker = ("CONAN_DOCKER_IMAGE" in os.environ) or (os.environ.get("CONAN_USE_DOCKER", False))
        if self.use_docker:
            conanfile = transplant_path(conanfile, os.getcwd(), self.docker_project)
        super(DockerMixin, self).__init__(conanfile=conanfile, *args, **kwargs)

    def set_compiler(self, compiler):
        if self.use_docker:
            docker_image = os.environ.get("CONAN_DOCKER_IMAGE", None)  # TODO: Implement auto-name based on compiler
            log.info("TravisRunner will use docker image '{}'".format(docker_image))
            self.docker_helper = DockerHelper(image=docker_image)
            self.docker_helper.pull()

            # Change conan storage/path
            self.conan_conf = ConanConf()
            new_storage = os.path.join(os.path.expanduser("~"), 'new_conan_storage')
            self.conan_conf.replace("storage", "path", new_storage)
            if not os.path.exists(new_storage):
                os.makedirs(new_storage)

            # Map some directories
            self.docker_helper.add_mount_unit(os.getcwd(), self.docker_project)
            self.docker_helper.add_mount_unit(os.path.expanduser("~"), self.docker_home)
            remote_storage = os.path.join(self.docker_home, '.conan', 'data'),  # TODO: It may be other
            self.docker_helper.add_mount_unit(new_storage, remote_storage)

            # Run the container
            self.docker_helper.run()

            # Install what is needed
            self.docker_helper.run_in_docker("sudo pip install -U conan conan_sword_and_sorcery=={version} && conan user".format(version=__version__))

            # Create profiles directory
            self.docker_helper.run_in_docker("sudo mkdir {profile_dir}".format(profile_dir=self.docker_profiles))

        super(DockerMixin, self).set_compiler(compiler)

    def set_profile(self, profile):
        tgt_name = os.path.join(self.docker_profiles, os.path.basename(profile))
        self.docker_helper.copy(profile, tgt_name)
        super(DockerMixin, self).set_profile(tgt_name)

    def change_conan_storage(self, new_storage):
        conan_conf = os.path.join(os.path.expanduser("~"), '.conan', 'conan.conf')
        # Read in the file
        with open(conan_conf, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('path = ~/.conan/data', "path = {}".format(new_storage))

        # Write the file out again
        with open(conan_conf, 'w') as file:
            file.write(filedata)

    def cmd(self, command):
        if not self.use_docker:
            return super(DockerMixin, self).cmd(command)
        else:
            if not self.dry_run:
                ret = self.docker_helper.run_in_docker(command)
                return SUCCESS if ret == 0 else FAIL
            return DRY_RUN
