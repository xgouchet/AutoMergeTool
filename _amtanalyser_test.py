#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import unittest

from amtanalyser import *

CFA_PATH = 'tests/unit/analyser/{0}.txt'


class ConflictedFileAnalyserTest(unittest.TestCase):
    def test_file_without_conflicts(self):
        # Given
        analyser = ConflictedFileAnalyser()
        file_path = CFA_PATH.format('no_conflicts')

        # When
        remaining = analyser.has_remaining_conflicts(file_path)

        # Then
        self.assertEqual(remaining, False)

    def test_file_with_1_conflict(self):
        # Given
        analyser = ConflictedFileAnalyser()
        file_path = CFA_PATH.format('single_conflict')

        # When
        remaining = analyser.has_remaining_conflicts(file_path)

        # Then
        self.assertEqual(remaining, True)

    def test_file_with_3_conflict(self):
        # Given
        analyser = ConflictedFileAnalyser()
        file_path = CFA_PATH.format('three_conflicts')

        # When
        remaining = analyser.has_remaining_conflicts(file_path)

        # Then
        self.assertEqual(remaining, True)


if __name__ == '__main__':
    unittest.main()
