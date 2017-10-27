#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace

from typing import List
from automergetool.amt_utils import *
from automergetool.amt_lcs import LCSAnalyser, StringSequencer, CommonSubSeq, DiffSubSeq


def parse_arguments(args: List[str]) -> Namespace:
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = ArgumentParser(description="A tool to resolve dummy conflicts")

    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument(
        '-r',
        '--report',
        choices=[REPORT_NONE, REPORT_SOLVED, REPORT_UNSOLVED, REPORT_FULL],
        default=REPORT_NONE,
        required=False)
    parser.add_argument('-v', '--verbose', required=False, action='store_true')

    return parser.parse_args(args)


def handle_conflict(conflict: Conflict, prompt):
    """Handle a conflicts here"""
    # get each side's content
    lines_local = conflict.local_lines()
    lines_base = conflict.base_lines()
    lines_remote = conflict.remote_lines()

    if len(lines_local) == 1 and len(lines_base) == 1 and len(lines_remote) == 1:
        base = lines_base[0]
        local = lines_local[0]
        remote = lines_remote[0]
        __handle_single_line_conflict(conflict, base, local, remote, prompt)


# noinspection PyUnresolvedReferences
def __handle_single_line_conflict(conflict: Conflict, base: str, local: str, remote: str, prompt):
    # Prevent recursion limit
    limit = sys.getrecursionlimit()
    max_size = max(len(base), len(local), len(remote))
    # Arbitrary threshold
    if max_size * 6 > limit:
        return

    # find common lines
    analyser = LCSAnalyser(StringSequencer())
    result = analyser.lcs_with_diff(base=base, left=local, right=remote)

    if len(result) == 0:
        return

    # iterate over sub sequences
    resolution = ""
    for ss in result:
        if type(ss) is CommonSubSeq:
            resolution += ss.content
        elif type(ss) is DiffSubSeq:
            if ss.content_b == ss.content_l:
                resolution += ss.content_r
            elif ss.content_b == ss.content_r:
                resolution += ss.content_l
            else:
                return

    if prompt(conflict, resolution):
        conflict.resolve(resolution)


def prompt_resolution(conflict: Conflict, resolution: str, user_input=lambda msg: input(msg)) -> bool:
    prompt = " ⋄ Single line conflict found:\n"
    prompt += conflict.raw
    prompt += "\n   Proposed resolution:\n"
    prompt += "— — — —\n" + resolution + "— — — —\n"
    prompt += "Apply the resolution ? (y/n)"

    choice = user_input(prompt)

    if choice.lower() == 'y':
        return True


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    walker = ConflictsWalker(args.merged, 'single_line', args.report, args.verbose)
    while walker.has_more_conflicts():
        handle_conflict(walker.next_conflict(), prompt_resolution)
    walker.end()
    sys.exit(walker.get_merge_status())
