#!/usr/bin/python
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

    def test_ignore_first(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_NONE)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_not_addition(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", " \n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda conflict: ORDER_REMOTE_FIRST)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_get_order_remote(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When handling the conflict
        order = get_order(conflict, ORDER_REMOTE_FIRST)

        # Then check the conflict is not resolved
        self.assertEqual(order, ORDER_REMOTE_FIRST)

    def test_get_order_local(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When handling the conflict
        order = get_order(conflict, ORDER_LOCAL_FIRST)

        # Then check the conflict is not resolved
        self.assertEqual(order, ORDER_LOCAL_FIRST)

    def test_get_order_ask_local(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When handling the conflict
        order = get_order(conflict, ORDER_ASK, lambda msg: "2")

        # Then check the conflict is not resolved
        self.assertEqual(order, ORDER_LOCAL_FIRST)

    def test_get_order_ask_remote(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When handling the conflict
        order = get_order(conflict, ORDER_ASK, lambda msg: "1")

        # Then check the conflict is not resolved
        self.assertEqual(order, ORDER_REMOTE_FIRST)

    def test_get_order_ask_none(self):
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When handling the conflict
        order = get_order(conflict, ORDER_ASK, lambda msg: "0")

        # Then check the conflict is not resolved
        self.assertEqual(order, ORDER_NONE)


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
