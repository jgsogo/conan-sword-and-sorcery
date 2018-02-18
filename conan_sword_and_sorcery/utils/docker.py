# -*- coding: utf-8 -*-

import os
import logging

log = logging.getLogger(__name__)


class DockerHelper(object):
    mnt = {}

    def __init__(self, image, name=None):
        self.image = image
        self.name = name or image.replace('/', '-')

    def __del__(self):
        self._stop()

    def pull(self):
        r = os.system("docker pull {}".format(self.image))
        if r != 0:
            raise RuntimeError("Error pulling docker image '{}'".format(self.image))

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
            mnt=' '.join(["-v {ori}:{tgt}" for ori, tgt in self.mnt.items()])
        )
        self._run()

    def _run(self):
        if self._running:
            self._stop()

        r = os.system(self._running)
        if r != 0:
            raise RuntimeError("Error running container")

    def _stop(self):
        r = os.system("docker stop {name}".format(name=self.name))
        self._running = None

    def copy(self, origin, tgt):
        r = os.system("docker cp {origin} {name}:{tgt}".format(
            origin=origin,
            name=self.name,
            tgt=tgt))
        if r != 0:
            raise RuntimeError("Error copying file to container")

    def run_in_docker(self, command):
        log.info("run_in_docker: {}".format(command))
        return os.system("docker exec -it {name} /bin/sh -c \"sudo {command}\"".format(
            name=self.docker_name, command=command
        ))
