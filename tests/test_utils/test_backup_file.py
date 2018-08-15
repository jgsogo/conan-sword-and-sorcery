# -*- coding: utf-8 -*-
import unittest
import tempfile
import shutil
import os

from conan_sword_and_sorcery.utils import backup_file


class TestBackupFile(unittest.TestCase):

    def run(self, *args, **kwargs):
        self.tmp_dir = tempfile.mkdtemp()
        try:
            file1 = tempfile.NamedTemporaryFile(mode="w", dir=self.tmp_dir, delete=False)
            file1.write("file1")
            file1.close()
            self.file1 = file1.name

            super(TestBackupFile, self).run(*args, **kwargs)
        finally:
            shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_invalid_file(self):
        with self.assertRaises(IOError):
            with backup_file("invented-file-name"):
                self.assertTrue(True)

    def test_deletion(self):
        original_content = open(self.file1).read()
        with backup_file(self.file1):
            self.assertTrue(os.path.exists(self.file1))
            os.remove(self.file1)
            self.assertFalse(os.path.exists(self.file1))
        self.assertTrue(os.path.exists(self.file1))
        self.assertEqual(original_content, open(self.file1).read())

    def test_content_restored(self):
        original_content = open(self.file1).read()
        with backup_file(self.file1):
            with open(self.file1, 'w') as f:
                f.write("more content")
            self.assertNotEqual(original_content, open(self.file1).read())
        self.assertEqual(original_content, open(self.file1).read())

    def test_collision_names(self):
        another_file = "{}.bak".format(self.file1)
        another_content = "another file with the expected name for backup"
        with open(another_file, "w") as f:
            f.write("another file with the expected name for backup")

        with backup_file(self.file1):
            self.assertTrue(True)

        self.assertTrue(os.path.exists(another_file))
        self.assertEqual(another_content, open(another_file).read())

