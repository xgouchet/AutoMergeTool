#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from amtutils import *


def parse_arguments():
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = argparse.ArgumentParser(description="A tool to resolve woven conflicts")

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
    """Handle a conflicts where the changes are woven"""
    lines_local = conflict.local_lines()
    lines_base = conflict.base_lines()
    lines_remote = conflict.remote_lines()
    if len(lines_local) != 0:
        return
    if len(lines_remote) != 0:
        return
    resolution = "\n"
    conflict.resolve(resolution)


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.merged, 'dels', args.report, args.verbose)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict())
    walker.end()
    sys.exit(walker.get_merge_status())
