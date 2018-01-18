#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from automergetool.amt_utils import Conflict
from automergetool.solvers.gen_woven import *


class SolverTest(unittest.TestCase):
    def test_simple(self):
        """Test a conflict with woven changes"""
        # Given a conflict
        conflict = fake_conflict("fool\nbar\neggs\n", "foo\nbar\neggs\n", "foo\nbaz\negg\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "fool\nbaz\negg\n")

    def test_not_woven_1(self):
        """Test a conflict with woven changes + additions"""
        # Given a conflict
        conflict = fake_conflict("fool\nbar\neggs\nspam\n", "foo\nbar\neggs\n", "foo\nbaz\negg\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_woven_2(self):
        """Test a conflict with woven changes + additions"""
        # Given a conflict
        conflict = fake_conflict("fool\nbar\neggs\n", "foo\nbar\neggs\n", "foo\nbaz\negg\nspam\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_woven_3(self):
        """Test a conflict with woven changes + deletions"""
        # Given a conflict
        conflict = fake_conflict("fool\neggs\n", "foo\nbar\neggs\n", "foo\nbaz\negg\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_woven_4(self):
        """Test a conflict with woven changes + deletions"""
        # Given a conflict
        conflict = fake_conflict("fool\nbar\neggs\n", "foo\nbar\neggs\n", "foo\negg\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_woven_5(self):
        """Test a conflict with real conflicts"""
        # Given a conflict
        conflict = fake_conflict("fool\nballs\nbacon\n", "foo\nbar\neggs\n", "foos\nbaz\negg\n")

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


if __name__ == '__main__':
    unittest.main()
