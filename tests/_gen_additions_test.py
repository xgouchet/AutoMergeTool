#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from automergetool.amt_utils import Conflict
from automergetool.solvers.gen_additions import *


class SolverTest(unittest.TestCase):
    def test_local_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_LOCAL_FIRST)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "foo\nbaz\n")

    def test_remote_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_FIRST)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "baz\nfoo\n")

    def test_local_only(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_LOCAL_ONLY)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "foo\n")

    def test_remote_only(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_ONLY)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "baz\n")

    def test_ignore_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_NONE)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_addition(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "spam\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_FIRST)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_addition_space_means_blank(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "spam\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_FIRST, True)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_addition_blank_lines_mean_empty(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", " \n\t \n \n\n \n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_FIRST, True)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "baz\nfoo\n")

    def test_addition_keep_blank_lines(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", " \n\t\n\n \n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_FIRST, False)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_same_addition_exact(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "", "foo\n")

        # When handling the conflict
        handle_conflict(conflict, lambda _c: ORDER_REMOTE_FIRST, False)

        # Then check the conflict is not resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "foo\n")

    def test_get_order_remote(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_REMOTE_FIRST)

        # Then check the order is correct
        self.assertEqual(order, ORDER_REMOTE_FIRST)

    def test_get_order_local(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_LOCAL_FIRST)

        # Then check the order is correct
        self.assertEqual(order, ORDER_LOCAL_FIRST)

    def test_get_order_ask_remote_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_ASK, lambda msg: "1")

        # Then check the order is correct
        self.assertEqual(order, ORDER_REMOTE_FIRST)

    def test_get_order_ask_local_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_ASK, lambda msg: "2")

        # Then check the order is correct
        self.assertEqual(order, ORDER_LOCAL_FIRST)

    def test_get_order_ask_remote_only(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_ASK, lambda msg: "3")

        # Then check the order is correct
        self.assertEqual(order, ORDER_REMOTE_ONLY)

    def test_get_order_ask_local_only(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_ASK, lambda msg: "4")

        # Then check the order is correct
        self.assertEqual(order, ORDER_LOCAL_ONLY)

    def test_get_order_ask_none(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When asking the order
        order = get_order(conflict, ORDER_ASK, lambda msg: "0")

        # Then check the order is correct
        self.assertEqual(order, ORDER_NONE)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_shorts(self):
        # Given
        m = "m"
        o = ORDER_REMOTE_FIRST
        r = REPORT_UNSOLVED

        # When
        parsed = parse_arguments(['-m', m, '-o', o, '-r', r, '-v', '-w'])

        self.assertEqual(parsed.merged, m)
        self.assertEqual(parsed.order, o)
        self.assertEqual(parsed.report, r)
        self.assertEqual(parsed.verbose, True)
        self.assertEqual(parsed.whitespace, True)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_long(self):
        # Given
        r = REPORT_FULL
        m = "m"
        o = ORDER_LOCAL_FIRST

        # When
        parsed = parse_arguments(['--order', o, '--merged', m, '--verbose', '--report', r, '--whitespace'])

        self.assertEqual(parsed.merged, m)
        self.assertEqual(parsed.order, o)
        self.assertEqual(parsed.report, r)
        self.assertEqual(parsed.verbose, True)
        self.assertEqual(parsed.whitespace, True)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_with_defaults(self):
        # Given
        m = "m"

        # When
        parsed = parse_arguments(['--merged', m])

        self.assertEqual(parsed.merged, m)
        self.assertEqual(parsed.order, ORDER_ASK)
        self.assertEqual(parsed.report, REPORT_NONE)
        self.assertEqual(parsed.verbose, False)
        self.assertEqual(parsed.whitespace, False)

    def test_missing_arguments(self):
        r = REPORT_NONE

        with self.assertRaises(SystemExit) as context:
            parse_arguments(['--report', r])

    def test_unknown_argument(self):
        r = REPORT_SOLVED
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parsed = parse_arguments(['-m', m, '-r', r, '--kamoulox', "foo"])

    def test_invalid_order_argument(self):
        o = "kamoulox"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parsed = parse_arguments(['-m', m, '-o', o])

    def test_invalid_report_argument(self):
        r = "r"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parsed = parse_arguments(['-m', m, '-r', r])


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
