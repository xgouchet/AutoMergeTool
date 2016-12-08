#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
from amtutils import ConflictsWalker


def parse_arguments():
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = argparse.ArgumentParser(
        description="A tool to combine multiple merge tools")

    parser.add_argument('-b', '--base', required=True)
    parser.add_argument('-l', '--local', required=True)
    parser.add_argument('-r', '--remote', required=True)
    parser.add_argument('-m', '--merged', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    walker = ConflictsWalker(args.base, args.local, args.remote, args.merged)
    while walker.has_more_conflicts():
        print (walker.next_conflict())
    sys.exit(walker.get_merge_status())
