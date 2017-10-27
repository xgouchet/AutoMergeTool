#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from automergetool.amt_utils import *


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

    return parser.parse_args()


def handle_conflict(conflict):
    """Handle a conflicts here"""
    # get each side's content
    base = conflict.base
    local = conflict.local
    remote = conflict.remote
    # Here's where you'd try to handle the conflict.
    # If it's possible to fix the conflict, call `conflict.resolve(resolution)`
    # Where resolution is the conflict's resolution, as it should appear in the final file
    # If you can't (or don't want to) resolve the conflict, leave the conflict as is


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.merged, 'mwc', args.report)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict())
    walker.end()
    sys.exit(walker.get_merge_status())
