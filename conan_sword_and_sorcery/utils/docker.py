# -*- coding: utf-8 -*-

import logging

from conan_sword_and_sorcery.utils.cmd import cmd

log = logging.getLogger(__name__)


class DockerHelper(object):
    mnt = {}
    _running = None

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
        if self._running:
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
        if self._running:
            self._stop()
        cmd(command=self._running, error_msg="Error running container: {command}")

    def _stop(self):
        cmd("docker stop {name}".format(name=self.name), exception=None)

    def copy(self, origin, tgt):
        command = "docker cp {origin} {name}:{tgt}".format(origin=origin, name=self.name, tgt=tgt)
        cmd(command, error_msg="Error copying file to container: {command}")

    def run_in_docker(self, command, sudo=True):
        sudoer = "sudo " if sudo else ''
        return cmd("docker exec -it {name} /bin/sh -c \"{sudoer}{command}\"".format(
            name=self.name, command=command, sudoer=sudoer
        ))
