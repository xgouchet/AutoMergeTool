#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from automergetool.amt_lcs import *


class StringSequencerLower(StringSequencer):
    def are_items_equal(self, a: str, b: str) -> bool:
        return a.lower() == b.lower()


class StringSequencerSeparated(StringSequencer):
    def concat(self, a: str, b: str) -> str:
        return a.upper() + ";" + b.upper()


class StringSequencerQuoted(StringSequencer):
    def box(self, item: str):
        return "‘" + str(item) + "’"


class LCSTest(unittest.TestCase):
    def test_empty(self):
        """Tests LCS for 3 empty strings"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencer())
        b = ""
        l = ""
        r = ""

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        self.assertEqual(result, [])

    def test_simple(self):
        """Tests LCS for 3 simple strings"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencer())
        b = "text"
        l = "fest"
        r = "melt"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [CommonSubSeq("e", 1, 1, 1), CommonSubSeq("t", 3, 3, 3)]
        self.assertEqual(result, expected)

    def test_medium(self):
        """Tests LCS for 3 medium strings"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencer())
        b = "Hell, this is a bad one !"
        l = "He called-on me."
        r = "Hey Bill, cook !"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [
            CommonSubSeq("He", 0, 0, 0), CommonSubSeq("ll", 2, 5, 6), CommonSubSeq("o", 20, 10, 12),
            CommonSubSeq(" ", 23, 12, 14)
        ]
        self.assertEqual(result, expected)

    def test_custom_comparator(self):
        """Tests LCS for 3 simple strings with custom comparator"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencerLower())
        b = "Hell, this is a bad one !"
        l = "He called-on me."
        r = "Hey Li, look out !"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [
            CommonSubSeq("He", 0, 0, 0), CommonSubSeq("l", 2, 5, 4), CommonSubSeq("l", 3, 6, 8),
            CommonSubSeq("o", 20, 10, 13), CommonSubSeq(" ", 23, 12, 16)
        ]
        self.assertEqual(result, expected)

    def test_custom_box(self):
        """Tests LCS for 3 simple strings with custom boxing"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencerQuoted())
        b = "contestant"
        l = "rightest"
        r = "testing"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [CommonSubSeq("‘t’‘e’‘s’‘t’", 3, 4, 0)]
        self.assertEqual(result, expected)

    def test_custom_concat(self):
        """Tests LCS for 3 simple strings with custom concatenator"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencerSeparated())
        b = "contestant"
        l = "rightest"
        r = "testing"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [CommonSubSeq("T;E;S;T", 3, 4, 0)]
        self.assertEqual(result, expected)

    def test_reorder(self):
        """Tests LCS for 3 simple strings, checking different order (commutativity)"""
        # Given strings to compare
        a = LCSAnalyser(ListSequencer())
        b = "acegikmoqsuwy"
        l = "abdeghjkmnpqstvwyz"
        r = "bcdfghjklnoprstvwx"

        # When computing lcs
        extract = lambda x: x.content
        result = list(map(extract, a.lcs(b, l, r)))

        # Then
        self.assertEqual(result, list(map(extract, a.lcs(b, r, l))))
        self.assertEqual(result, list(map(extract, a.lcs(l, b, r))))
        self.assertEqual(result, list(map(extract, a.lcs(l, r, b))))
        self.assertEqual(result, list(map(extract, a.lcs(r, b, l))))
        self.assertEqual(result, list(map(extract, a.lcs(r, l, b))))

    def test_simple_with_diff(self):
        """Tests LCS for 3 simple strings"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencer())
        b = "text"
        l = "fest"
        r = "melt"

        # When computing lcs
        result = a.lcs_with_diff(b, l, r)

        # Then
        expected = [DiffSubSeq("t", "f", "m", 0, 0, 0),
                    CommonSubSeq("e", 1, 1, 1),
                    DiffSubSeq("x", "s", "l", 2, 2, 2),
                    CommonSubSeq("t", 3, 3, 3)]
        self.assertEqual(result, expected)

    def test_medium_with_diff(self):
        """Tests LCS for 3 medium strings"""
        # Given strings to compare
        a = LCSAnalyser(StringSequencer())
        b = "Hell, this is a bad one !"
        l = "He called-on me."
        r = "Hey Bill, cook !"

        # When computing lcs
        result = a.lcs_with_diff(b, l, r)

        # Then
        expected = [
            CommonSubSeq("He", 0, 0, 0),
            DiffSubSeq("", " ca", "y Bi", 2, 2, 2),
            CommonSubSeq("ll", 2, 5, 6),
            DiffSubSeq(", this is a bad ", "ed-", ", co", 4, 7, 8),
            CommonSubSeq("o", 20, 10, 12),
            DiffSubSeq("ne", "n", "k", 21, 11, 13),
            CommonSubSeq(" ", 23, 12, 14),
            DiffSubSeq("!", "me.", "!", 24, 13, 15)
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
