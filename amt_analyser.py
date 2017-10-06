#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from amt_utils import CONFLICT_START, CONFLICT_SEP, CONFLICT_BASE, CONFLICT_END


class ConflictedFileAnalyser:
    """
    This class will check if a file has remaining unsolved conflicts
    """

    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def has_remaining_conflicts(self, file_path: str) -> bool:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith(CONFLICT_START) \
                        or line.startswith(CONFLICT_SEP) \
                        or line.startswith(CONFLICT_BASE) \
                        or line.startswith(CONFLICT_END):
                    return True

        return False


if __name__ == '__main__':
    print("This is just a utility module, not to be launched directly.")
    sys.exit(1)
