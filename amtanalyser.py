#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from amtutils import CONFLICT_START, CONFLICT_SEP, CONFLICT_BASE, CONFLICT_END


class ConflictedFileAnalyser:
    """
    This class will check if a file has remaining unsolved conflicts
    """

    def __init__(self):
        pass

    def has_remaining_conflicts(self, file):
        with open(file, 'r') as f:
            for line in f:
                if line.startswith(CONFLICT_START) \
                        or line.startswith(CONFLICT_SEP) \
                        or line.startswith(CONFLICT_BASE) \
                        or line.startswith(CONFLICT_END):
                    return True

        return False
