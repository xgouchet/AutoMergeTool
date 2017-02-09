#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from _gen_solver import *


class SolverTest(unittest.TestCase):
    def test_can_solve(self):
        """Test a conflict with foo"""
        # Given a conflict
        conflict = fake_conflict("foo\n", "bar\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.resolution, "eggs")

    def test_cant_solve(self):
        """Test a conflict which can be shrunk"""
        # Given a conflict
        conflict = fake_conflict("abc\n", "xyz\n", "123\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is not resolved, nor rewritten
        self.assertFalse(conflict.is_resolved())
        self.assertFalse(conflict.is_rewritten())


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote, "<<<<<<<\n", ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
