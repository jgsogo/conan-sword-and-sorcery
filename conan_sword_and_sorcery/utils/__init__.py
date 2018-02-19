# -*- coding: utf-8 -*-

import contextlib
import os
import shutil


try:
    basestring  # attempt to evaluate basestring

    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)


def slice(total, current_page, total_pages):
    assert current_page > 0, "current_page ({}) must be equal to '1' or more (do not zero index)".format(current_page)
    assert current_page <= total_pages, "current_page ({}) cannot be greater than total_pages ({})".format(current_page, total_pages)
    assert total >= total_pages, "total ({}) must be at least equal to 'total_pages' ({})".format(total, total_pages)

    current_page = current_page - 1  # Make it zero indexed

    page_size = total // total_pages
    remain = total - (page_size * total_pages)
    init = (page_size + 1) * min(current_page, remain) + page_size * max(0, current_page - remain)
    end = init + page_size + (1 if current_page < remain else 0)
    return init, end


@contextlib.contextmanager
def backup_file(filename, backup_dir=None):
    backup_dir = backup_dir or os.path.dirname(filename)
    backup_filename = os.path.basename(filename) + ".bak"
    i = 1
    while os.path.exists(os.path.join(backup_dir, backup_filename)):
        backup_filename = os.path.basename(filename) + ".bak.{}".format(i)
        i += 1

    shutil.copy2(filename, os.path.join(backup_dir, backup_filename))
    try:
        yield
    finally:
        shutil.copy2(os.path.join(backup_dir, backup_filename), filename)
        os.remove(os.path.join(backup_dir, backup_filename))