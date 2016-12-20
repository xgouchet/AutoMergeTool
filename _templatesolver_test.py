#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest

from solver import *


class SolverTest(unittest.TestCase):
    def test_foo(self):
        """Test a conflict with foo"""
        # Given a conflict
        conflict = fake_conflict("foo\n", "bar\n", "baz\n")

        # When handling the conflict
        handle_conflict(conflict)

        # Then check the conflict is resolved
        self.assertTrue(conflict.is_resolved())
        self.assertEqual(conflict.resolution, "eggs")
        # ... or not
        self.assertFalse(conflict.is_resolved())


def fake_conflict(local, base, remote):
    return Conflict(local, base, remote,
                    "<<<<<<<\n" + local + "|||||||\n" + base + "=======\n" + remote + ">>>>>>>\n")


if __name__ == '__main__':
    unittest.main()
