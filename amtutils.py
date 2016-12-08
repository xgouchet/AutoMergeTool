#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


class ConflictsWalker:
    """
    ConflictsWalker is a utility class that can iterate over conflicts regions
    and rewrite the merged file if needed
    """


    def __init__(self, merged):
        self.conflicted = merged
        self.merged = merged + ".resolving.amt"
        self.conflicted_file = open(conflicted)
        self.merged_file = open(merged, 'w')

    def has_more_conflicts(self):
        # move forward in conflicted read / merged write until a conflict is found
        return False

    def next_conflict(self):
        return Nil

    def get_merge_status(self):
        return 1

if __name__ == '__main__':
    print ("This is a utility module, not to be launched by itself, except for tests.")
    sys.exit(1)
