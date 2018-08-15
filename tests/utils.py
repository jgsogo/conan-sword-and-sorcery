# -*- coding: utf-8 -*-
import re
import subprocess

import unittest

from conan_sword_and_sorcery.utils.environ import clean_context_env, context_env
from conan_sword_and_sorcery.ci.compilers import CompilerRegistry


class TestCaseEnvClean(unittest.TestCase):
    _initial_context_env = {}

    def run(self, *args, **kwargs):
        with clean_context_env(pattern="^(CONAN_.*)|(TRAVIS)|(APPVEYOR)$"):  # TODO: What else?
            with context_env(**self._initial_context_env):
                super(TestCaseEnvClean, self).run(*args, **kwargs)


def count_registered_compilers(id=None, osys=None, **kwargs):
    id = id if isinstance(id, list) or id is None else [id, ]
    osys = osys if isinstance(osys, list) or osys is None else [osys, ]
    compiler_kwargs = {}
    for k, v in kwargs.items():
        value = v if isinstance(v, list) or v is None else [v, ]
        compiler_kwargs[k] = value

    n = 0
    for class_holder in CompilerRegistry._registry:
        if id and class_holder.compiler_class.id not in id:
            continue
        if osys and class_holder.compiler_class.osys not in osys:
            continue

        def validate_compiler(instance):
            for key, value in compiler_kwargs.items():
                compiler_key_value = getattr(instance, key, None)
                if compiler_key_value and compiler_key_value not in value:
                    return False
            return True

        n += sum([validate_compiler(instance) for instance in class_holder.explode()])

    return n


def parse_remote_list():
    remote_line = re.compile(r'^(.*): (http[^\[\s]+)(\s*\[Verify SSL: True\]\s*)?$')
    remotes = subprocess.check_output(["conan", "remote", "list"]).decode('utf-8')
    ret = []
    for item in remotes.split('\n'):
        if not len(item.strip()):
            continue
        m = remote_line.match(item)
        name = m.group(1)
        url = m.group(2)
        ret.append((name, url))
    return ret