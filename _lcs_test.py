#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from lcs import *

class LCSTest(unittest.TestCase):

    def test_empty(self):
        """Tests LCS for 3 empty strings"""
        # Given strings to compare
        b = ""
        l = ""
        r = ""

        # When computing lcs
        result = lcs(b, l, r)

        # Then
        #self.assertEquals(result, "")

    def test_simple(self):
        """Tests LCS for 3 simple strings"""
        # Given strings to compare
        b = "text"
        l = "fest"
        r = "melt"

        # When computing lcs
        result = lcs(b, l, r)

        # Then
        expected = [Subsequence("e", 1, 1, 1), Subsequence("t", 3, 3, 3)]
        self.assertEqual(result, expected)

    def test_simple(self):
        """Tests LCS for 3 simple strings"""
        # Given strings to compare
        b = "Hell, this is a bad one !"
        l = "He called-on me."
        r = "Hey Bill, look out !"

        # When computing lcs
        result = lcs(b, l, r)

        # Then
        expected = [Subsequence("He", 0, 0, 0), Subsequence("ll", 2, 5, 6), Subsequence("o", 20,10,11), Subsequence(" ", 23,12,14)]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
