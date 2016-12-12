#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import filecmp
from amtutils import *

class ConflictTest(unittest.TestCase):


    def test_no_conflicts(self):
        walker = ConflictsWalker('tests/unit/conflict_walker/no_conflicts.txt', '', REPORT_NONE)
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)
        self.assertTrue(filecmp.cmp(walker.merged, 'tests/unit/conflict_walker/no_conflicts.txt'))

    def test_single_conflict_unsolved(self):
        walker = ConflictsWalker('tests/unit/conflict_walker/single_conflict.txt', '', REPORT_NONE)
        self.assertTrue(walker.has_more_conflicts())
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)
        self.assertTrue(filecmp.cmp(walker.merged, 'tests/unit/conflict_walker/single_conflict.txt'))

    def test_single_conflict_solved(self):
        walker = ConflictsWalker('tests/unit/conflict_walker/single_conflict.txt', '', REPORT_NONE)
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()
        conflict.resolve("Nunc quis interdum nunc. Praesent mollis risus enim, at elementum quam finibus ut.\n")
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)
        self.assertTrue(filecmp.cmp(walker.merged, 'tests/unit/conflict_walker/single_conflict_resolved.txt'))

    def test_missing_base_side(self):
        walker = ConflictsWalker('tests/unit/conflict_walker/missing_base.txt', '', REPORT_NONE)


if __name__ == '__main__':
    unittest.main()
