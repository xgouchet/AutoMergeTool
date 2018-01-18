#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string
import unittest

from automergetool.amt_utils import Conflict
from automergetool.solvers.gen_simplify import *


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

    def test_stack_overflow(self):
        """Test a conflict which too many lines"""
        # Given a conflict
        sys.setrecursionlimit(500)
        size = 100
        conflict = fake_conflict(generateRandom(size), generateRandom(size), generateRandom(size))

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    # noinspection PyUnresolvedReferences
    def test_path_arguments_shorts(self):
        # Given
        r = REPORT_UNSOLVED
        m = "m"

        # When
        parsed = parse_arguments(['-m', m, '-r', r, '-v'])

        self.assertEqual(parsed.report, r)
        self.assertEqual(parsed.merged, m)
        self.assertEqual(parsed.verbose, True)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_long(self):
        # Given
        r = REPORT_FULL
        m = "m"

        # When
        parsed = parse_arguments(['--merged', m, '--verbose', '--report', r])

        self.assertEqual(parsed.report, r)
        self.assertEqual(parsed.merged, m)
        self.assertEqual(parsed.verbose, True)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_with_defaults(self):
        # Given
        m = "m"

        # When
        parsed = parse_arguments(['--merged', m])

        self.assertEqual(parsed.report, REPORT_NONE)
        self.assertEqual(parsed.merged, m)
        self.assertEqual(parsed.verbose, False)

    def test_missing_arguments(self):
        r = REPORT_NONE

        with self.assertRaises(SystemExit) as context:
            parse_arguments(['--report', r])

    def test_unknown_argument(self):
        r = REPORT_SOLVED
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parsed = parse_arguments(['-m', m, '-r', r, '--kamoulox', "foo"])

    def test_invalid_argument(self):
        r = "r"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parsed = parse_arguments(['-m', m, '-r', r])


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


def generateRandom(lines):
    result = ""
    for i in range(0, lines, 1):
        result += random.choice(string.ascii_letters + string.digits) + "\n"
    return result


if __name__ == '__main__':
    unittest.main()
