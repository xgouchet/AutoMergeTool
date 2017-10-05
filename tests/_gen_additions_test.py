#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from gen_additions import *


class SolverTest(unittest.TestCase):
    def test_local_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_LOCAL_FIRST)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "foo\nbaz\n")

    def test_remote_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_REMOTE_FIRST)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "baz\nfoo\n")

    def test_local_only(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_LOCAL_ONLY)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "foo\n")

    def test_remote_only(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_REMOTE_ONLY)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "baz\n")

    def test_ignore_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_NONE)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_addition(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "spam\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_REMOTE_FIRST)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_addition_space_means_blank(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "spam\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_REMOTE_FIRST, True)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_addition_blank_lines_mean_empty(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", " \n\t \n \n\n \n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_REMOTE_FIRST, True)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "baz\nfoo\n")

    def test_addition_keep_blank_lines(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", " \n\t\n\n \n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda c: ORDER_REMOTE_FIRST, False)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_same_addition_exact(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "", "foo\n")

        # When handling the conflict
        handle_conflict(conflict, lambda c: ORDER_REMOTE_FIRST, False)

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


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
