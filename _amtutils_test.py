#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import filecmp
import os
from amtutils import *

CW_PATH = 'tests/unit/conflict_walker/{0}.txt'

RESOLUTION = "Nunc quis interdum nunc. Praesent mollis risus enim, at elementum quam finibus ut.\n"


class ConflictTest(unittest.TestCase):
    def test_no_conflicts(self):
        """Tests a walker against a file without conflicts"""

        # Given a file to merge
        file = CW_PATH.format('no_conflicts')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)

        # Then check the output
        self.assertTrue(filecmp.cmp(walker.merged, file))
        self.assertEqual(walker.get_merge_status(), 0)
        os.remove(walker.merged)

    def test_single_conflict_unsolved(self):
        """Tests a walker against a file with a single conflict, without solving it"""

        # Given a file to merge
        file = CW_PATH.format('single_conflict')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        self.assertTrue(walker.has_more_conflicts())
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)

        # Then check the output
        self.assertTrue(filecmp.cmp(walker.merged, file))
        self.assertEqual(walker.get_merge_status(), 1)
        os.remove(walker.merged)

    def test_single_conflict_solved(self):
        """Tests a walker against a file with a single conflict, and solving it"""

        # Given a file to merge
        file = CW_PATH.format('single_conflict')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()
        conflict.resolve(RESOLUTION)
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)

        # Then check the output
        self.assertTrue(filecmp.cmp(walker.merged, CW_PATH.format('single_conflict_resolved')))
        self.assertEqual(walker.get_merge_status(), 0)
        os.remove(walker.merged)

    def test_two_conflicts_half_solved_with_full_report(self):
        """Tests a walker against a file with two conflicts, and solving one of them"""

        # Given a file to merge
        file = CW_PATH.format('two_conflicts')
        walker = ConflictsWalker(file, 'test', REPORT_FULL)

        # When walking the conflicts
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()
        conflict.resolve(RESOLUTION)
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()  # not solved
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)

        # Then check the output
        self.assertTrue(filecmp.cmp(walker.merged, CW_PATH.format('two_conflicts_half_solved')))
        self.assertTrue(
            filecmp.cmp(file + '.test-report',
                        CW_PATH.format('two_conflicts_half_solved') + '.test-full-report'))
        self.assertEqual(walker.get_merge_status(), 1)
        os.remove(walker.merged)

    def test_two_conflicts_half_solved_with_solved_report(self):
        """Tests a walker against a file with two conflicts, and solving one of them"""

        # Given a file to merge
        file = CW_PATH.format('two_conflicts')
        walker = ConflictsWalker(file, 'test', REPORT_SOLVED)

        # When walking the conflicts
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()
        conflict.resolve(RESOLUTION)
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()  # not solved
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)

        # Then check the output
        self.assertTrue(filecmp.cmp(walker.merged, CW_PATH.format('two_conflicts_half_solved')))
        self.assertTrue(
            filecmp.cmp(file + '.test-report',
                        CW_PATH.format('two_conflicts_half_solved') + '.test-solved-report'))
        self.assertEqual(walker.get_merge_status(), 1)
        os.remove(walker.merged)

    def test_two_conflicts_half_solved_with_unsolved_report(self):
        """Tests a walker against a file with two conflicts, and solving one of them"""

        # Given a file to merge
        file = CW_PATH.format('two_conflicts')
        walker = ConflictsWalker(file, 'test', REPORT_UNSOLVED)

        # When walking the conflicts
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()
        conflict.resolve(RESOLUTION)
        self.assertTrue(walker.has_more_conflicts())
        conflict = walker.next_conflict()  # not solved
        self.assertFalse(walker.has_more_conflicts())
        walker.end(False)

        # Then check the output
        self.assertTrue(filecmp.cmp(walker.merged, CW_PATH.format('two_conflicts_half_solved')))
        self.assertTrue(
            filecmp.cmp(file + '.test-report',
                        CW_PATH.format('two_conflicts_half_solved') + '.test-unsolved-report'))
        self.assertEqual(walker.get_merge_status(), 1)
        os.remove(walker.merged)

    def test_missing_base_side(self):
        """Tests a walker against a file with conflicts without the `diff3` conflict style"""

        # Given a file to merge
        file = CW_PATH.format('missing_base')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        with self.assertRaises(RuntimeError):
            walker.has_more_conflicts()

        walker.end(False)
        os.remove(walker.merged)

    def test_invalid_conflict_section_1(self):
        """Tests a walker against a file with invalid conflict section"""

        # Given a file to merge
        file = CW_PATH.format('invalid_conflict_1')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        with self.assertRaises(RuntimeError):
            walker.has_more_conflicts()

        walker.end(False)
        os.remove(walker.merged)

    def test_invalid_conflict_section_2(self):
        """Tests a walker against a file with invalid conflict section"""

        # Given a file to merge
        file = CW_PATH.format('invalid_conflict_2')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        with self.assertRaises(RuntimeError):
            walker.has_more_conflicts()

        walker.end(False)
        os.remove(walker.merged)

    def test_invalid_conflict_section_3(self):
        """Tests a walker against a file with invalid conflict section"""

        # Given a file to merge
        file = CW_PATH.format('invalid_conflict_3')
        walker = ConflictsWalker(file, '', REPORT_NONE)

        # When walking the conflicts
        with self.assertRaises(RuntimeError):
            walker.has_more_conflicts()

        walker.end(False)
        os.remove(walker.merged)



if __name__ == '__main__':
    unittest.main()
