#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import List

from amt_utils import CONFLICT_START, CONFLICT_SEP, CONFLICT_BASE, CONFLICT_END


class ImportsSolver(ABC):
    """
    Defines an import conflicts solver class, ie: a solver handling conflicts in the import
    section of a source file

    This is an abstract class and can be extended to handle the syntax specifics of any language,
    assuming that import statements are always on a single line, and are grouped in the source file.
    """

    def __init__(self):
        super().__init__()

    def solve_import_conflicts(self,
                               base_path: str,
                               local_path: str,
                               remote_path: str,
                               merged_path: str) -> bool:
        """
        Main method used to handle the conflicts in the given fileset
        :param base_path: the base version path
        :param local_path: the local version path
        :param remote_path: the remote version path
        :param merged_path: the merged version path
        :return: whether the file is conflict-free
        """
        # check if there are conflicts to resolve
        if not (self.__has_imports_conflicts(merged_path)):
            print("No imports conflicts we can help with, ignored")
            return False

        merged_imports = self.__get_merge_imports(base_path, local_path, remote_path)
        (section_start, section_end) = self.__find_import_section_range(merged_path)

        return self.replace_imports_section(merged_path, merged_imports, section_start, section_end)

    def __has_imports_conflicts(self, merged_path: str) -> bool:
        """
        Check if the given file has any conflicts in the imports section
        """
        in_conflict = False
        conflict_has_import = False
        conflict_has_non_import = False
        conflicts_with_imports = 0

        with open(merged_path) as f:
            for line in f:
                if in_conflict:
                    if line.startswith(CONFLICT_END):
                        in_conflict = False
                        if conflict_has_import:
                            if conflict_has_non_import:
                                # this conflict mixes import and non import content, ignore
                                return False
                            else:
                                conflicts_with_imports += 1
                    elif line.startswith(CONFLICT_SEP) or line.startswith(CONFLICT_BASE):
                        continue
                    elif self.is_import_line(line):
                        conflict_has_import = True
                    elif not self.is_allowed_within_import_section(line):
                        conflict_has_non_import = True
                elif line.startswith(CONFLICT_START):
                    in_conflict = True
                    conflict_has_import = False
                    conflict_has_non_import = False

        return conflicts_with_imports > 0

    def __get_merge_imports(self, base_path: str, local_path: str, remote_path: str) -> List[str]:
        """
        Resolve the imports that should appear in the merged file
        base_path -- the path to the base file
        local_path -- the path to the local file
        remote_path -- the path to the remote file
        """
        imports_base = self.__read_imports(base_path)
        imports_local = self.__read_imports(local_path)
        imports_remote = self.__read_imports(remote_path)

        return self.__merge_imports(imports_base, imports_local, imports_remote)

    def __merge_imports(self, imp_base: List[str], imp_local: List[str],
                        imp_remote: List[str]) -> List[str]:
        """
        Merge imports from various lists
        :param imp_base: the base imports
        :param imp_local: the local imports
        :param imp_remote: the remote imports
        :return: the merged imports list
        """
        imports_merged = []

        # handle imports present in the three files
        for imp in imp_base:
            if (imp in imp_local) and (imp in imp_remote):
                imports_merged.append(imp)
                imp_local.remove(imp)
                imp_remote.remove(imp)

        # imports added in the local
        for imp in imp_local:
            if (imp not in imports_merged) and (imp not in imp_base):
                imports_merged.append(imp)

        # imports added in the REMOTE
        for imp in imp_remote:
            if (imp not in imports_merged) and (imp not in imp_base):
                imports_merged.append(imp)

        return imports_merged

    def __read_imports(self, path: str) -> List[str]:
        """
        Reads all imports from the given file and return them in a list
        filename -- the path to the file to read
        """
        imports = []  # type: list
        with open(path) as f:
            content = f.readlines()
            for line in content:
                if self.is_import_line(line):
                    imports.append(line)
        return sorted(imports)

    def __find_import_section_range(self, path: str) -> (int, int):
        section_start = -1
        last_import_in_section = -1
        in_conflict = False
        in_section = False
        conflict_start = 0
        conflict_content = ""
        conflict_has_imports = False

        with open(path) as f:
            content = f.readlines()
            for i, line in enumerate(content):
                if in_conflict:
                    if line.startswith(CONFLICT_END):
                        in_conflict = False
                        if conflict_has_imports:
                            if not in_section:
                                in_section = True
                                section_start = conflict_start
                            last_import_in_section = i
                    elif self.is_import_line(line):
                        conflict_has_imports = True
                        last_import_in_section = i
                else:
                    if line.startswith(CONFLICT_START):
                        in_conflict = True
                        conflict_start = i
                    elif self.is_import_line(line):
                        if not in_section:
                            in_section = True
                            section_start = i
                        last_import_in_section = i
                    elif in_section and not self.is_allowed_within_import_section(line):
                        section_end = i - 1
                        break

        return section_start, last_import_in_section

    def __write_merged_imports(self, file: TextIOWrapper, imports: list):
        """
        Sorts and write the given imports to the file, adding a blank line between
        each group
        f -- the file object (needs write permission)
        imports -- the list of imports
        """
        sorted_imports = self.sort_imports(imports)
        previous_group = -1
        for imp in sorted_imports:
            group = self.get_import_group(imp)
            if not (group == previous_group):
                if not (previous_group == -1):
                    file.write("\n")
                previous_group = group
            file.write(imp)

    def sort_imports(self, imports: list) -> list:
        """
        :param imports: the list of imports to sort
        :return: a list with the same imports, sorted as necessary
        """
        return sorted(sorted(imports), key=lambda imp: self.get_import_group(imp))

    def replace_imports_section(self,
                                merged_path: str,
                                merged_imports: list,
                                section_start: int,
                                section_end: int) -> bool:
        """
        Rewrites the given file, replacing the import section with the merged imports
        :param merged_path: the path of the file to rewrite
        :param merged_imports: the merged imports to write
        :param section_start: the first line index of the old imports section
        :param section_end:  the last line index of the old imports section
        :return: whether the file is conflict-free at the end of the process
        """
        # First read the original content
        with open(merged_path) as f:
            content = f.readlines()

        # Then rewrite it with the merges in place
        merged_imports_written = False
        conflicts_remain = False
        with open(merged_path, 'w') as f:
            for i, line in enumerate(content):
                if i < section_start or i > section_end:
                    f.write(line)
                    if line.startswith(CONFLICT_START) or line.startswith(CONFLICT_START) or \
                            line.startswith(CONFLICT_START) or line.startswith(CONFLICT_START):
                        conflicts_remain = True
                elif not merged_imports_written:
                    self.__write_merged_imports(f, merged_imports)
                    merged_imports_written = True

        return not conflicts_remain

    @abstractmethod
    def is_import_line(self, line: str) -> bool:
        """
        :param line: a single line from the source file
        :return: whether the line is considered an import statement
        """
        pass

    @abstractmethod
    def is_allowed_within_import_section(self, line: str) -> bool:
        """
        :param line: a single line from the source file
        :return: whether the line is a non import statement, but allowed within an import section
        (eg: empty line)
        Note that those lines won't appear at all in the merged files, so if the user have comments in the import
        section, you might want to not keep those
        """
        pass

    @abstractmethod
    def get_import_group(self, imp: str) -> int:
        """
        :param imp: an import statement
        :return: the group in which the statement belongs; when written, imports are ordered by group
        (smallest to highest), and alphabetically within a group
        For a more custom sort, you can override the sort_imports() method
        """
        pass
