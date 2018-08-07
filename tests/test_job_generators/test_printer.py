# -*- coding: utf-8 -*-

import os
import unittest

from conan_sword_and_sorcery.job_generators.printer import print_jobs
from conan_sword_and_sorcery.ci.compilers.clang import CompilerClangApple


class PrinterTests(unittest.TestCase):

    def test_no_jobs(self):
        def output(msg):
            if not hasattr(output, "_full_msg"):
                output._full_msg = ""
            output._full_msg += msg
        print_jobs(all_jobs=[], printer=output)
        self.assertEqual(output._full_msg, "There are no jobs!\n")

    def test_print_no_job_status(self):
        def output(msg):
            if not hasattr(output, "_full_msg"):
                output._full_msg = ""
            output._full_msg += msg

        jobs = [(CompilerClangApple(arch='x86', build_type='Release', version='8.1', libcxx='libstdc++'), {'option1': 'value1', 'option2': 'value2', }),
                (CompilerClangApple(arch='x86', build_type='Release', version='8.1', libcxx='libstdc++'), {})]
        print_jobs(all_jobs=jobs, printer=output)
        self.assertEqual(output._full_msg,
"""+-------------+-----------+--------+--------------+-----------+-----------+-----------+
| id          |   version | arch   | build_type   | libcxx    | option1   | option2   |
|-------------+-----------+--------+--------------+-----------+-----------+-----------|
| apple-clang |       8.1 | x86    | Release      | libstdc++ | value1    | value2    |
| apple-clang |       8.1 | x86    | Release      | libstdc++ |           |           |
+-------------+-----------+--------+--------------+-----------+-----------+-----------+
""")

    def test_print_with_job_status(self):
        def output(msg):
            if not hasattr(output, "_full_msg"):
                output._full_msg = ""
            output._full_msg += msg

        jobs = [(CompilerClangApple(arch='x86', build_type='Release', version='8.1', libcxx='libstdc++'), {'option1': 'value1', 'option2': 'value2', }),
                (CompilerClangApple(arch='x86', build_type='Release', version='8.1', libcxx='libstdc++'), {})]
        print_jobs(all_jobs=jobs, printer=output, job_status=["ST1", "ST2"])
        self.assertEqual(output._full_msg,
"""+----------+-------------+-----------+--------+--------------+-----------+-----------+-----------+
| status   | id          |   version | arch   | build_type   | libcxx    | option1   | option2   |
|----------+-------------+-----------+--------+--------------+-----------+-----------+-----------|
| ST1      | apple-clang |       8.1 | x86    | Release      | libstdc++ | value1    | value2    |
| ST2      | apple-clang |       8.1 | x86    | Release      | libstdc++ |           |           |
+----------+-------------+-----------+--------+--------------+-----------+-----------+-----------+
""")
