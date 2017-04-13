#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from amtutils import *

ORDER_LOCAL_FIRST = "localfirst"
ORDER_LOCAL_ONLY = "localonly"
ORDER_REMOTE_FIRST = "remotefirst"
ORDER_REMOTE_ONLY = "remoteonly"
ORDER_ASK = "ask"
ORDER_NONE = ""


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
    parser.add_argument('-w', '--whitespace', required=False, action='store_true')
    parser.add_argument('-v', '--verbose', required=False, action='store_true')

    return parser.parse_args()


def is_same_addition(local, remote):
    # TODO allow some margin of error in this check (different whitespace, comments...)
    return local == remote


def handle_conflict(conflict, chose_order, space_means_empty=False):
    """Handle a conflicts where the base is empty"""

    # Check if is addition
    if conflict.base != "":
        if space_means_empty:
            if not conflict.base.isspace():
                return
        else:
            return

    # Check if same addition in remote and local
    if is_same_addition(conflict.local, conflict.remote):
        conflict.resolve(conflict.local)
        return

    # get the order
    order = chose_order(conflict)

    if order == ORDER_REMOTE_FIRST:
        conflict.resolve(conflict.remote + conflict.local)
    elif order == ORDER_LOCAL_FIRST:
        conflict.resolve(conflict.local + conflict.remote)
    elif order == ORDER_REMOTE_ONLY:
        conflict.resolve(conflict.remote)
    elif order == ORDER_LOCAL_ONLY:
        conflict.resolve(conflict.local)


def get_order(conflict, choice, user_input=lambda msg: input(msg)):
    use_order = choice
    while use_order == ORDER_ASK:
        prompt = "Addition conflict found. Which one should we use first ?\n\n"
        prompt += "<<<<<<< LOCAL\n" + conflict.local
        prompt += ">>>>>>> REMOTE\n" + conflict.remote
        prompt += "Select action : \n"
        prompt += " - [1] Remote First\n"
        prompt += " - [2] Local First\n"
        prompt += " - [3] Remote Only\n"
        prompt += " - [4] Local Only\n"
        prompt += " - [0] Ignore conflict\n"
        prompt += "»"
        choice = user_input(prompt)
        if choice == '0':
            use_order = ORDER_NONE
        elif choice == '1':
            use_order = ORDER_REMOTE_FIRST
        elif choice == '2':
            use_order = ORDER_LOCAL_FIRST
        elif choice == '3':
            use_order = ORDER_REMOTE_ONLY
        elif choice == '4':
            use_order = ORDER_LOCAL_ONLY
    return use_order


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.merged, 'adds', args.report, args.verbose)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict(), lambda conflict: get_order(conflict, args.order),
                        args.whitespace)
    walker.end()
    sys.exit(walker.get_merge_status())
