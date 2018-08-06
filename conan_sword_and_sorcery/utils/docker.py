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
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    for key, value in os.environ.items():
        # Check this issue https://github.com/moby/moby/issues/12997
        #   and provided solution (commented in the issue): https://gist.github.com/hudon/149466af21dfc52fdc70
        if key.startswith(('CONAN', 'TRAVIS', )):
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
        self._running = "docker run {{env_file}} {options} {mnt} --name {name} --detach {image}".format(
            options='-t' if allocate_tty else '',
            name=self.name,
            image=self.image,
            mnt=' '.join(["-v {}:{}".format(ori, tgt) for ori, tgt in self.mnt.items()])
        )
        self._run()

    def _run(self):
        if self._is_running:
            self._stop()
        with temporary_env_file() as env_file:
            env_file_param = "--env-file={}".format(env_file)
            cmd(command=self._running.format(env_file=env_file_param), error_msg="Error running container: {command}")
        self._is_running = True

    def _stop(self):
        cmd("docker stop {name}".format(name=self.name), exception=None)
        self._is_running = False

    def copy(self, origin, tgt):
        command = "docker cp {origin} {name}:{tgt}".format(origin=origin, name=self.name, tgt=tgt)
        cmd(command, error_msg="Error copying file to container: {command}")

    def run_in_docker(self, command, sudo=True):
        sudoer = "sudo " if sudo else ''
        return cmd("docker exec {name} /bin/sh -c \"{sudoer}{command}\"".format(
            name=self.name, command=command, sudoer=sudoer
        ))
