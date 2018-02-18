# -*- coding: utf-8 -*-
import os
import logging

from conan_sword_and_sorcery import __version__

log = logging.getLogger(__name__)


def transplant_path(fullpath, ori_rel, tgt_rel):
    return os.path.join(tgt_rel, os.path.relpath(fullpath, ori_rel))


class DockerMixin(object):
    docker_name = 'conan_docker'
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
            self.docker_image = os.environ.get("CONAN_DOCKER_IMAGE", None)  # TODO: Implement auto-name based on compiler
            log.info("TravisRunner will use docker image '{}'".format(self.docker_image))
            self.pull_image()
        super(DockerMixin, self).set_compiler(compiler)

    def set_profile(self, profile):
        tgt_name = os.path.join(self.docker_profiles, os.path.basename(profile))
        os.system("docker cp {origin} {name}:{tgt}".format(origin=profile, name=self.docker_name, tgt=tgt_name))
        super(DockerMixin, self).set_profile(tgt_name)

    def pull_image(self):
        os.system("docker pull {}".format(self.docker_image))

        # Change local storage
        local_storage = os.path.join(os.path.expanduser("~"), 'new_conan_storage')
        self.change_conan_storage(local_storage)
        os.makedirs(local_storage)

        # Run detached
        os.system("docker run -t"
                  " -v {cwd}:{docker_dirname}"
                  " -v {local_storage}:{remote_storage}"
                  " -v {host_home}:{docker_home}"
                  " --name {name} --detach {image}".format(
            cwd=os.getcwd(),
            docker_dirname=self.project,
            host_home=os.path.expanduser("~"),
            docker_home=self.docker_home,
            local_storage=local_storage,
            remote_storage=os.path.join(self.docker_home, '.conan', 'data'),  # TODO: It may be other
            name=self.docker_name,
            image=self.docker_image)
        )

        # Install what is needed
        self.run_in_docker("sudo pip install -U conan conan_sword_and_sorcery=={version} && conan user".format(version=__version__))

        # Create profiles directory
        self.run_in_docker("sudo mkdir {profile_dir}".format(profile_dir=self.profiles))

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
            return self.run_in_docker(command)

    def run_in_docker(self, command):
        log.info("run_in_docker: {}".format(command))
        if not self.dry_run:
            ret = os.system("docker exec -it {name} /bin/sh -c \"sudo {command}\"".format(name=self.docker_name, command=command))
            return "OK" if ret == 0 else "FAIL"
        return "DRY_RUN"
