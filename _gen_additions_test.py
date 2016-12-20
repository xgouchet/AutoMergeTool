#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest

from gen_additions import *


class SolverTest(unittest.TestCase):
    def test_local_first(self):
        """Test a conflict with additions"""
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda: ORDER_LOCAL_FIRST)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.resolution, "foo\nbaz\n")

    def test_remote_first(self):
        """Test a conflict with additions"""
        # Given a conflict
        conflict = fake_conflict("foo\n", '', "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda: ORDER_REMOTE_FIRST)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.resolution, "baz\nfoo\n")

    def test_not_addition(self):
        """Test an unsolvable conflict"""
        # Given a conflict
        conflict = fake_conflict("foo\n", "\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict, lambda: ORDER_REMOTE_FIRST)

        # Then check the conflict is not resolved
        self.assertFalse(conflict.is_resolved())


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote,
                    "<<<<<<<\n" + local + "|||||||\n" + base + "=======\n" + remote + ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
