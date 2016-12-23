#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
from amtutils import *

ORDER_LOCAL_FIRST = "localfirst"
ORDER_REMOTE_FIRST = "remotefirst"
ORDER_ASK = "ask"


def parse_arguments():
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = argparse.ArgumentParser(description="A tool to resolve addition conflicts")

    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument(
        '-o',
        '--order',
        choices=[ORDER_LOCAL_FIRST, ORDER_REMOTE_FIRST, ORDER_ASK],
        default=ORDER_REMOTE_FIRST,
        required=False)
    parser.add_argument(
        '-r',
        '--report',
        choices=[REPORT_NONE, REPORT_SOLVED, REPORT_UNSOLVED, REPORT_FULL],
        default=REPORT_NONE,
        required=False)
    parser.add_argument('-v', '--verbose', required=False, action='store_true')

    return parser.parse_args()


def handle_conflict(conflict, order):
    """Handle a conflicts where the base is empty"""
    if (conflict.base != ""):
        return
    use_order = order()

    if use_order == ORDER_REMOTE_FIRST:
        conflict.resolve(conflict.remote + conflict.local)
    elif use_order == ORDER_LOCAL_FIRST:
        conflict.resolve(conflict.local + conflict.remote)


def __get_order(choice):
    use_order = choice
    while use_order == ORDER_ASK:
        print("Addition conflict found. Which one should we use first ?\n")
        print("<<<<<<< LOCAL")
        print(conflict.local)
        print(">>>>>>> REMOTE")
        print(conflict.remote)
        choice = input(
            "Select action : [1] Remote First / [2] Local First / [0] Ignore conflict : ")
        if choice == '0':
            return
        elif choice == '1':
            use_order = ORDER_REMOTE_FIRST
        elif choice == '2':
            use_order = ORDER_LOCAL_FIRST
    return use_order


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.merged, 'adds', args.report, args.verbose)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict(), lambda: __get_order(args.order))
    walker.end()
    sys.exit(walker.get_merge_status())
