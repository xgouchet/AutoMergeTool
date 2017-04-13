#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from gen_deletions import *


class SolverTest(unittest.TestCase):
    def test_simple(self):
        """Test a conflict with deletions"""
        # Given a conflict
        conflict = fake_conflict("\n", "foo\nbar\neggs\n", "\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.content, "\n")

    def test_no_deletion(self):
        """Test a conflict with no deletions"""
        # Given a conflict
        conflict = fake_conflict("foo\n", "foo\nbar\neggs\n", "spam\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_remote_deletion(self):
        """Test a conflict with no deletions"""
        # Given a conflict
        conflict = fake_conflict("foo\n", "foo\nbar\neggs\n", "\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())

    def test_local_deletion(self):
        """Test a conflict with no deletions"""
        # Given a conflict
        conflict = fake_conflict("\n", "foo\nbar\neggs\n", "foo\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
