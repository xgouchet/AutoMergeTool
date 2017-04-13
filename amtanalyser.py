#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from amtutils import *


class ConflictedFileAnalyser:
    """
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
