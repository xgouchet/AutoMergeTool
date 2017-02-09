#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from gen_simplify import *


class SolverTest(unittest.TestCase):
    def test_simplify_split(self):
        """Test a conflict which can be split in too"""
        # Given a conflict
        conflict = fake_conflict("foo\nbar\nbacon\n", "bar\n", "bar\neggs\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertEqual(conflict.content, "<<<<<<<\nfoo\n|||||||\n=======\n>>>>>>>\n" + "bar\n" +
                         "<<<<<<<\nbacon\n|||||||\n=======\neggs\n>>>>>>>\n")

    def test_simplify_shrink(self):
        """Test a conflict which can be shrunk"""
        # Given a conflict
        conflict = fake_conflict("foo\nbar\nspam\nbacon\n", "foo\nbacon\n",
                                 "foo\nbaz\neggs\nbacon\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertEqual(
            conflict.content,
            "foo\n" + "<<<<<<<\nbar\nspam\n|||||||\n=======\nbaz\neggs\n>>>>>>>\n" + "bacon\n")

    def test_simplify_multiple_split(self):
        """Test a conflict which can be split in n"""
        # Given a conflict
        conflict = fake_conflict("a\nz\ny\nb\nc\nd\ne\nf\nx\n", "a\n2\n3\n4\nb\nc\nd\n5\n6\ne\nf\n",
                                 "0\na\n1\nb\nc\nd\n7\ne\n8\n9\nf\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertEqual(conflict.content, "<<<<<<<\n|||||||\n=======\n0\n>>>>>>>\n" + "a\n" +
                         "<<<<<<<\nz\ny\n|||||||\n2\n3\n4\n=======\n1\n>>>>>>>\n" + "b\nc\nd\n" +
                         "<<<<<<<\n|||||||\n5\n6\n=======\n7\n>>>>>>>\n" + "e\n" +
                         "<<<<<<<\n|||||||\n=======\n8\n9\n>>>>>>>\n" + "f\n" +
                         "<<<<<<<\nx\n|||||||\n=======\n>>>>>>>\n")

    def test_simplify_split_deletions(self):
        """Test a conflict which can be split in n"""
        # Given a conflict
        conflict = fake_conflict("a\nb\n", "a\nb\nc\n", "b\nc\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertEqual(conflict.content, "<<<<<<<\na\n|||||||\na\n=======\n>>>>>>>\n" + "b\n" +
                         "<<<<<<<\n|||||||\nc\n=======\nc\n>>>>>>>\n")

    def test_cant_simplify(self):
        """Test a conflict which can be shrunk"""
        # Given a conflict
        conflict = fake_conflict("a\nb\nc\n", "x\ny\nz\n", "1\n2\n3\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
