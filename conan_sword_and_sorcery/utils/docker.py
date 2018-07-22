# -*- coding: utf-8 -*-

import os
import logging
from contextlib import contextmanager
import tempfile

from conan_sword_and_sorcery.utils.cmd import cmd

log = logging.getLogger(__name__)


@contextmanager
def temporary_env_file():
    # Log env variables into a file to use it afterwards: https://stackoverflow.com/questions/30494050/how-do-i-pass-environment-variables-to-docker-containers
    "--env-file ./env.list"
    tmp = tempfile.NamedTemporaryFile(delete=False)
    for key, value in os.environ.items():
        tmp.write("{}={}\n".format(key, value))
    tmp.close()
    try:
        yield tmp.name
    finally:
        os.remove(tmp.name)


class DockerHelper(object):
    mnt = {}
    _running = None
    _is_running = False

    def __init__(self, image, name=None):
        self.image = image
        self.name = name or image.replace('/', '_')

    def __del__(self):
        self._stop()

    def pull(self):
        command = "docker pull {}".format(self.image)
        cmd(command, error_msg="Error pulling docker image '{}': {{command}}".format(self.image))

    def add_mount_unit(self, host, target):
        if host in self.mnt:
            log.warning("Host '{}' is already mounted to '{}'. Will override it.".format(host, self.mnt[host]))
        self.mnt[host] = target
        if self._is_running:
            self._run()

    def run(self, allocate_tty=True):
        self._running = "docker run {options} {mnt} --name {name} --detach {image}".format(
            options='-t' if allocate_tty else '',
            name=self.name,
            image=self.image,
            mnt=' '.join(["-v {}:{}".format(ori, tgt) for ori, tgt in self.mnt.items()])
        )
        self._run()

    def _run(self):
        if self._is_running:
            self._stop()
        cmd(command=self._running, error_msg="Error running container: {command}")
        self._is_running = True

    def _stop(self):
        cmd("docker stop {name}".format(name=self.name), exception=None)
        self._is_running = False

    def copy(self, origin, tgt):
        command = "docker cp {origin} {name}:{tgt}".format(origin=origin, name=self.name, tgt=tgt)
        cmd(command, error_msg="Error copying file to container: {command}")

    def run_in_docker(self, command, sudo=True):
        sudoer = "sudo " if sudo else ''
        with temporary_env_file() as env_file:
            return cmd("docker exec --env-file={} -it {name} /bin/sh -c \"{sudoer}{command}\"".format(
                env_file,
                name=self.name, command=command, sudoer=sudoer
            ))
