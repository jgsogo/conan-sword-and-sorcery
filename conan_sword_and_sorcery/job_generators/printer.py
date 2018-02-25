# -*- coding: utf-8 -*-
import sys


def print_jobs(all_jobs, printer=sys.stdout.write, job_status=None):
    compiler_headers_ext = set()
    option_headers = set()
    for compiler, options in all_jobs:
        compiler_headers_ext.update(compiler._data.keys())
        option_headers.update(options.keys())

    compiler_headers = ['id', 'version', 'arch', 'build_type']
    compiler_headers += [it for it in compiler_headers_ext if it not in compiler_headers]

    table = []
    for i, (compiler, options) in enumerate(all_jobs):
        status = [job_status[i]] if job_status else []
        table.append(status +
                     [getattr(compiler, it, '') for it in compiler_headers] +
                     [options.get(it, '') for it in option_headers])

    if len(table):
        from tabulate import tabulate

        if job_status:
            assert len(all_jobs) == len(job_status), "You must provide a status for every job"
            compiler_headers = ['status', ] + compiler_headers

        printer(tabulate(table, headers=list(compiler_headers)+list(option_headers),
                         # showindex=True,
                         tablefmt='psql'))
        printer("\n")
    else:
        sys.stdout.write("There are no jobs!\n")
