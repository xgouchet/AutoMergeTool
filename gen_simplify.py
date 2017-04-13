#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from amtlcs import *
from amtutils import *


def parse_arguments():
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = argparse.ArgumentParser(description="A tool to resolve dummy conflicts")

    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument(
        '-r',
        '--report',
        choices=[REPORT_NONE, REPORT_SOLVED, REPORT_UNSOLVED, REPORT_FULL],
        default=REPORT_NONE,
        required=False)
    parser.add_argument('-v', '--verbose', required=False, action='store_true')

    return parser.parse_args()


def handle_conflict(conflict):
    """Handles a conflict which can be simplified"""

    # TODO override comparator to ignore \s+
    lines_local = conflict.local_lines()
    lines_base = conflict.base_lines()
    lines_remote = conflict.remote_lines()

    # Prevent recursion limit
    limit = sys.getrecursionlimit()
    max_size = max(len(lines_base), len(lines_local), len(lines_remote))
    # Arbitrary threshold
    if max_size * 6 > limit:
        return

    # find common lines
    analyser = LCSAnalyser(concatenate=lambda a, b: list(a) + list(b))
    result = analyser.lcs(l=lines_local, b=lines_base, r=lines_remote)

    if len(result) == 0:
        return

    # split conflicts
    ib = il = ir = 0
    resolution = ""
    for sub in result:
        if (sub.pos_b > ib) or (sub.pos_l > il) or (sub.pos_r > ir):
            # write conflict before subsequence
            resolution += conflict.marker_local
            for line in lines_local[il:sub.pos_l]:
                resolution += line
            resolution += CONFLICT_BASE + "\n"
            for line in lines_base[ib:sub.pos_b]:
                resolution += line
            resolution += CONFLICT_SEP + "\n"
            for line in lines_remote[ir:sub.pos_r]:
                resolution += line
            resolution += conflict.marker_remote

        # write subsequence
        size = len(list(sub.content))
        for line in list(sub.content):
            resolution += line

        # increment indices
        ib = sub.pos_b + size
        il = sub.pos_l + size
        ir = sub.pos_r + size

    if (ib < len(lines_base)) or (il < len(lines_local)) or (ir < len(lines_remote)):
        resolution += conflict.marker_local
        for line in lines_local[il:]:
            resolution += line
        resolution += CONFLICT_BASE + "\n"
        for line in lines_base[ib:]:
            resolution += line
        resolution += CONFLICT_SEP + "\n"
        for line in lines_remote[ir:]:
            resolution += line
        resolution += conflict.marker_remote

    conflict.rewrite(resolution)


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.merged, 'simplify', args.report, args.verbose)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict())
    walker.end()
    sys.exit(walker.get_merge_status())
