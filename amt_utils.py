#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional

CONFLICT_START = "<<<<<<<"
CONFLICT_BASE = "|||||||"
CONFLICT_SEP = "======="
CONFLICT_END = ">>>>>>>"

REPORT_NONE = "none"
REPORT_SOLVED = "solved"
REPORT_UNSOLVED = "unsolved"
REPORT_FULL = "full"

SUCCESSFUL_MERGE = 0
ERROR_NO_TOOL = 1
ERROR_EXTENSION = 2
ERROR_UNKNOWN = 3
ERROR_CONFLICTS = 4
ERROR_UNTRUSTED = 5
ERROR_INVOCATION = 6

# TODO add docstrings for this file


class Conflict:
    """
    Describes a conflict : it contains the base, local and remote
    versions
    """

    def __init__(self, local: str, base: str, remote: str, marker_local: str, marker_remote: str):
        self.local = local
        self.base = base
        self.remote = remote
        self.marker_local = marker_local
        self.marker_remote = marker_remote
        self.raw = marker_local + local + CONFLICT_BASE + "\n" + base + CONFLICT_SEP + "\n" + remote + marker_remote
        self.content = None
        self.resolved = False

    def resolve(self, resolution: str):
        self.content = resolution
        self.resolved = True

    def rewrite(self, content: str):
        self.content = content

    def is_rewritten(self) -> bool:
        return self.content is not None

    def is_resolved(self) -> bool:
        return self.resolved

    def local_lines(self) -> list:
        return Conflict.__lines(self.local)

    def base_lines(self) -> list:
        return Conflict.__lines(self.base)

    def remote_lines(self) -> list:
        return Conflict.__lines(self.remote)

    @staticmethod
    def __lines(block: str) -> list:
        lines = block.split('\n')
        filtered = list(filter(lambda x: len(x) > 0, lines))
        mapped = list(map(lambda x: x + "\n", filtered))
        return mapped


class ConflictsWalker:
    """
    ConflictsWalker is a utility class that can iterate over conflicts regions
    and rewrite the merged file if needed
    """

    def __init__(self,
                 merged_path: str,
                 report_name: Optional[str]=None,
                 report_type: str=REPORT_NONE,
                 verbose: bool=False):
        self.verbose = verbose
        self.log_tag = report_name
        self.conflicted = merged_path
        self.merged = merged_path + ".resolving.amt"
        self.conflicted_file = open(self.conflicted)
        self.merged_file = open(self.merged, 'w')
        self.conflict = None
        self.has_remaining_conflicts = False
        if report_name and report_type and report_type != REPORT_NONE:
            self.report_file = open(merged_path + "." + report_name + "-report", 'w')
            self.report_type = report_type
        else:
            self.report_file = None
            self.report_type = REPORT_NONE

    def has_more_conflicts(self) -> bool:
        self.write_previous_conflict()
        self.write_previous_conflict_report()
        self.log_previous_conflict()
        self.conflict = None

        # if has current conflict, write it or the resolution to the merged file
        conflict_started = False
        conflict_ended = False
        eof = False
        raw_conflict = ""
        sections = ["", "", ""]
        markers = ["", ""]
        section_index = 0
        sections_filled = 0
        while (not eof) and (not (conflict_started and conflict_ended)):
            line = self.conflicted_file.readline()
            if line == "":
                eof = True
            if line.startswith(CONFLICT_END):
                if not conflict_started:
                    raise RuntimeError("Found conflict ending tag without starting tag")
                if sections_filled != 3:
                    raise RuntimeError("Conflict is missing the base content. Try running : \n"
                                       "$ git config --global merge.conflictstyle diff3")
                raw_conflict += line
                markers[1] = line
                conflict_ended = True
            elif line.startswith(CONFLICT_START):
                conflict_started = True
                markers[0] = line
                raw_conflict += line
                section_index = 0
                sections_filled += 1
            elif line.startswith(CONFLICT_BASE):
                if not conflict_started:
                    raise RuntimeError("Found conflict base tag without starting tag")
                raw_conflict += line
                section_index = 1
                sections_filled += 1
            elif line.startswith(CONFLICT_SEP):
                if not conflict_started:
                    raise RuntimeError("Found conflict separation tag without starting tag")
                raw_conflict += line
                section_index = 2
                sections_filled += 1
            else:
                if conflict_started:
                    raw_conflict += line
                    sections[section_index] += line
                else:
                    self.merged_file.write(line)
        if eof:
            return False
        else:
            self.conflict = Conflict(sections[0], sections[1], sections[2], markers[0], markers[1])
            return True

    def next_conflict(self) -> Conflict:
        return self.conflict

    def end(self, apply: bool=True):
        self.conflicted_file.close()
        self.merged_file.close()

        if apply:
            os.rename(self.merged, self.conflicted)

        if self.report_file:
            self.report_file.close()

    def get_merge_status(self) -> int:
        """
        Returns the global merge status to report
        Either SUCCESSFUL_MERGE or one of the ERROR_xxx constants
        """
        if self.has_remaining_conflicts:
            return ERROR_CONFLICTS
        else:
            return SUCCESSFUL_MERGE

    def write_previous_conflict(self):
        """
        Writes the last conflict to the merged file (either the resolution or the original conflict)
        """
        if self.conflict is not None:
            if self.conflict.is_rewritten():
                self.merged_file.write(self.conflict.content)
            else:
                self.merged_file.write(self.conflict.raw)
            if not self.conflict.resolved:
                self.has_remaining_conflicts = True

    def write_previous_conflict_report(self):
        """
        Writes the last seen conflict in the report file
        """
        if self.report_file and self.report_type != REPORT_NONE:
            if self.conflict is not None:
                if self.conflict.is_resolved():
                    if (self.report_type == REPORT_SOLVED) or (self.report_type == REPORT_FULL):
                        self.report_file.write("\n*******  CONFLICT  *******\n")
                        self.report_file.write(self.conflict.raw)
                        self.report_file.write("\nv v v v RESOLUTION v v v v\n")
                        self.report_file.write(self.conflict.content)

                elif self.conflict.is_rewritten():
                    if (self.report_type == REPORT_UNSOLVED) or (self.report_type == REPORT_FULL):
                        self.report_file.write("\n*******  CONFLICT  *******\n")
                        self.report_file.write(self.conflict.raw)
                        self.report_file.write("\nv v v v RE-WRITTEN v v v v\n")
                        self.report_file.write(self.conflict.content)

                elif (self.report_type == REPORT_UNSOLVED) or (self.report_type == REPORT_FULL):
                    self.report_file.write("\n××××××× UNRESOLVED ×××××××\n")
                    self.report_file.write(self.conflict.raw)

    def log_previous_conflict(self):
        """
        Logs the last seen conflict in the standard output
        """
        if self.verbose:
            if self.conflict is not None:
                print(self.conflict.raw)

                if self.conflict.is_resolved():
                    print("     ✓ [" + self.log_tag + "] Solved")
                    print(self.conflict.content)
                elif self.conflict.is_rewritten():
                    print("     ↔ [" + self.log_tag + "] Rewritten")
                    print(self.conflict.content)
                else:
                    print("     ✗ [" + self.log_tag + "] Unsolved")


if __name__ == '__main__':
    print("This is just a utility module, not to be launched directly.")
    sys.exit(1)
