#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from amtlcs import *


class LCSTest(unittest.TestCase):
    def test_empty(self):
        """Tests LCS for 3 empty strings"""
        # Given strings to compare
        a = LCSAnalyser(boxing=lambda s: str(s))
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
        a = LCSAnalyser(boxing=lambda s: str(s))
        b = "text"
        l = "fest"
        r = "melt"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [Subsequence("e", 1, 1, 1), Subsequence("t", 3, 3, 3)]
        self.assertEqual(result, expected)

    def test_medium(self):
        """Tests LCS for 3 medium strings"""
        # Given strings to compare
        a = LCSAnalyser(boxing=lambda s: str(s))
        b = "Hell, this is a bad one !"
        l = "He called-on me."
        r = "Hey Bill, cook !"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [
            Subsequence("He", 0, 0, 0), Subsequence("ll", 2, 5, 6), Subsequence("o", 20, 10, 12),
            Subsequence(" ", 23, 12, 14)
        ]
        self.assertEqual(result, expected)

    def test_custom_comparator(self):
        """Tests LCS for 3 simple strings with custom comparator"""
        # Given strings to compare
        a = LCSAnalyser(comparator=lambda a, b: a.lower() == b.lower(), boxing=lambda s: str(s))
        b = "Hell, this is a bad one !"
        l = "He called-on me."
        r = "Hey Li, look out !"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [
            Subsequence("He", 0, 0, 0), Subsequence("l", 2, 5, 4), Subsequence("l", 3, 6, 8),
            Subsequence("o", 20, 10, 13), Subsequence(" ", 23, 12, 16)
        ]
        self.assertEqual(result, expected)

    def test_custom_concat(self):
        """Tests LCS for 3 simple strings with custom concatenator"""
        # Given strings to compare
        a = LCSAnalyser(
            concatenate=lambda a, b: a.upper() + ";" + b.upper(), boxing=lambda s: str(s))
        b = "contestant"
        l = "rightest"
        r = "testing"

        # When computing lcs
        result = a.lcs(b, l, r)

        # Then
        expected = [Subsequence("T;E;S;T", 3, 4, 0)]
        self.assertEqual(result, expected)

    def test_reorder(self):
        """Tests LCS for 3 simple strings, checking different order (commutativity)"""
        # Given strings to compare
        a = LCSAnalyser()
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


if __name__ == '__main__':
    unittest.main()
