#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
from amtutils import *


def parse_arguments():
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = argparse.ArgumentParser(
        description="A tool to resolve woven conflicts")

    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument(
        '-r',
        '--report',
        choices=[REPORT_NONE, REPORT_SOLVED, REPORT_UNSOLVED, REPORT_FULL],
        default=REPORT_NONE,
        required=False)

    return parser.parse_args()


def handle_conflict(conflict):
    """Handle a conflicts where the changes are woven"""
    lines_local = conflict.local.split('\n')
    lines_base = conflict.base.split('\n')
    lines_remote = conflict.remote.split('\n')
    if len(lines_local) != len(lines_base):
        return
    if len(lines_remote) != len(lines_base):
        return
    lines_count = len(lines_base)
    resolution = ""
    for l in range(lines_count):
        if lines_local[l] == lines_base[l]:
            resolution += lines_remote[l] + '\n'
        elif lines_remote[l] == lines_base[l]:
            resolution += lines_local[l] + '\n'
        else:
            # neither match, harder conflict, return early
            return
    # all lines solved :)
    conflict.resolve(resolution)


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.merged, 'mwc', args.report)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict())
    walker.end()
    sys.exit(walker.get_merge_status())
