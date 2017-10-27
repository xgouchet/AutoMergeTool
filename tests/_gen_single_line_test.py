#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from automergetool.amt_utils import Conflict
from automergetool.solvers.gen_single_line import *


def prompt_accept(conflict: Conflict, resolution: str) -> bool:
    return True


def prompt_refuse(conflict: Conflict, resolution: str) -> bool:
    return False


def user_input(msg: str, result: str) -> str:
    # print(msg)
    return result


class SolverTest(unittest.TestCase):
    def test_solvable_simple(self):
        """Test a conflict with modifications on the same line in different places"""
        # Given a conflict
        conflict = fake_conflict("callMe(true, 0, 'x');\n", "callMe(false, 0, 'x');\n", "callMe(false, 0, 'y');\n")

        # When handling the conflict
        handle_conflict(conflict, prompt_accept)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "callMe(true, 0, 'y');\n")

    def test_solvable_multiple(self):
        """Test a conflict with modifications on the same line in different places"""
        # Given a conflict
        conflict = fake_conflict("val foo = callMeX(true, 0, 'x');\n",
                                 "var foo = callMe(false, 0, 'x');\n",
                                 "var bar = callMe(false, 0, 'y');\n")

        # When handling the conflict
        handle_conflict(conflict, prompt_accept)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "val bar = callMeX(true, 0, 'y');\n")

    def test_solvable_multiple_not_accepted(self):
        """Test a conflict with modifications on the same line in different places"""
        # Given a conflict
        conflict = fake_conflict("val foo = callMeX(true, 0, 'x');\n",
                                 "var foo = callMe(false, 0, 'x');\n",
                                 "var bar = callMe(false, 0, 'y');\n")

        # When handling the conflict
        handle_conflict(conflict, prompt_refuse)

        # Then check the conflict is not resolved, nor rewritten
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_cant_solve(self):
        """Test a conflict which can be solved"""
        # Given a conflict
        conflict = fake_conflict("abc\n", "xyz\n", "123\n")

        # When handling the conflict
        handle_conflict(conflict, prompt_accept)

        # Then check the conflict is not resolved, nor rewritten
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_prompt_accept(self):
        """Test the prompt is done correctly"""
        # Given a conflict and resolution
        conflict = fake_conflict("abc\n", "xyz\n", "123\n")
        resolution = "jkl\n"

        # When prompting the user
        result = prompt_resolution(conflict, resolution, lambda msg: user_input(msg, 'y'))

        # Then check the conflict is resolved
        self.assertTrue(result)

    def test_prompt_refuse(self):
        """Test the prompt is done correctly"""
        # Given a conflict and resolution
        conflict = fake_conflict("abc\n", "xyz\n", "123\n")
        resolution = "jkl\n"

        # When prompting the user
        result = prompt_resolution(conflict, resolution, lambda msg: user_input(msg, 'n'))

        # Then check the conflict is resolved
        self.assertFalse(result)

    def test_path_argument_shorts(self):
        # Given
        m = "m"

        # When
        parsed = parse_arguments(['-m', m])

        # Then
        self.assertEqual(parsed.merged, m)

    def test_path_argument_long(self):
        # Given
        m = "m"

        # When
        parsed = parse_arguments(['--merged', m])

        # Then
        self.assertEqual(parsed.merged, m)

    def test_missing_argument(self):
        with self.assertRaises(SystemExit) as context:
            parse_arguments([])

    def test_unknown_argument(self):
        # Given
        m = "m"

        # Then
        with self.assertRaises(SystemExit) as context:
            parse_arguments(['--merged', m, '--kamoulox', '-p'])

    def test_report_argument_short(self):
        m = "m"
        report = REPORT_UNSOLVED

        # When
        parsed = parse_arguments(['--merged', m, '-r', report])

        # Then
        self.assertEqual(parsed.report, report)
        self.assertFalse(parsed.verbose)

    def test_report_argument_long(self):
        m = "m"
        report = REPORT_FULL

        # When
        parsed = parse_arguments(['--merged', m, '--report', report])

        # Then
        self.assertEqual(parsed.report, report)
        self.assertFalse(parsed.verbose)

    def test_report_argument_invalid(self):
        m = "m"
        report = "piubgpz"

        # When
        with self.assertRaises(SystemExit) as context:
            parsed = parse_arguments(['--merged', m, '--report', report])

    def test_verbose_argument_short(self):
        m = "m"
        report = REPORT_UNSOLVED

        # When
        parsed = parse_arguments(['--merged', m, '-v'])

        # Then
        self.assertTrue(parsed.verbose)

    def test_verbose_argument_long(self):
        m = "m"
        report = REPORT_FULL

        # When
        parsed = parse_arguments(['--merged', m, '--verbose'])

        # Then
        self.assertTrue(parsed.verbose)


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
