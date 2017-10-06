#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from filecmp import cmp
from shutil import copyfile

from amt_import_solver import *

IS_PATH = 'tests/data/import_solver/{0}.txt'


class ImportsSolverTest(unittest.TestCase):
    def test_no_import_statement(self):
        class NotAnImportsSolver(ImportsSolver):
            def is_import_line(self, line: str) -> bool:
                return False

            def is_allowed_within_import_section(self, line: str) -> bool:
                return False

            def get_import_group(self, imp: str) -> int:
                return 0

        # Given files
        base = IS_PATH.format("base")
        local = IS_PATH.format("local")
        remote = IS_PATH.format("remote")
        merged = IS_PATH.format("merged")
        merged_src = IS_PATH.format("merged_src")
        copyfile(merged_src, merged)  # reset merged file

        # When
        solver = NotAnImportsSolver()

        # Then
        result = solver.solve_import_conflicts(base, local, remote, merged)
        self.assertFalse(result)
        self.assertTrue(cmp(merged_src, merged, shallow=False))  # merged is untouched

    def test_no_import_conflicts(self):
        class DependsImportsSolver(ImportsSolver):
            def is_import_line(self, line: str) -> bool:
                return line.startswith("depends ")

            def is_allowed_within_import_section(self, line: str) -> bool:
                return line.startswith("# ") or line.isspace()

            def get_import_group(self, imp: str) -> int:
                return 0

        # Given files
        base = IS_PATH.format("base")
        local = IS_PATH.format("local")
        remote = IS_PATH.format("remote")
        merged = IS_PATH.format("merged")
        merged_src = IS_PATH.format("merged_src")
        copyfile(merged_src, merged)  # reset merged file

        # When
        solver = DependsImportsSolver()

        # Then
        result = solver.solve_import_conflicts(base, local, remote, merged)
        self.assertFalse(result)
        self.assertTrue(cmp(merged_src, merged, shallow=False))  # merged is untouched

    def test_mixed_import_conflicts(self):
        class DependsImportsSolver(ImportsSolver):
            def is_import_line(self, line: str) -> bool:
                return line.startswith("with ")

            def is_allowed_within_import_section(self, line: str) -> bool:
                return line.startswith("# ") or line.isspace()

            def get_import_group(self, imp: str) -> int:
                return 0

        # Given files
        base = IS_PATH.format("base")
        local = IS_PATH.format("local")
        remote = IS_PATH.format("remote")
        merged = IS_PATH.format("merged")
        merged_src = IS_PATH.format("merged_src")
        copyfile(merged_src, merged)  # reset merged file

        # When
        solver = DependsImportsSolver()

        # Then
        result = solver.solve_import_conflicts(base, local, remote, merged)
        self.assertFalse(result)
        self.assertTrue(cmp(merged_src, merged, shallow=False))  # merged is untouched

    def test_conflict_addition_blank_section(self):
        class IncludeImportsSolver(ImportsSolver):
            def is_import_line(self, line: str) -> bool:
                return line.startswith("include ")

            def is_allowed_within_import_section(self, line: str) -> bool:
                return line.startswith("# ") or line.isspace()

            def get_import_group(self, imp: str) -> int:
                return 0

        # Given files
        base = IS_PATH.format("base")
        local = IS_PATH.format("local")
        remote = IS_PATH.format("remote")
        merged = IS_PATH.format("merged")
        merged_src = IS_PATH.format("merged_src")
        copyfile(merged_src, merged)  # reset merged file

        # When
        solver = IncludeImportsSolver()

        # Then
        result = solver.solve_import_conflicts(base, local, remote, merged)
        self.assertFalse(result)
        self.assertTrue(cmp(IS_PATH.format("merged_solved_includes"), merged,
                            shallow=False))  # merged is untouched

    def test_conflict_complex_mixed_section(self):
        class ImportImportsSolver(ImportsSolver):
            def is_import_line(self, line: str) -> bool:
                return line.startswith("import ")

            def is_allowed_within_import_section(self, line: str) -> bool:
                return line.startswith("# ") or line.isspace()

            def get_import_group(self, imp: str) -> int:
                return 0

        # Given files
        base = IS_PATH.format("base")
        local = IS_PATH.format("local")
        remote = IS_PATH.format("remote")
        merged = IS_PATH.format("merged")
        merged_src = IS_PATH.format("merged_src")
        copyfile(merged_src, merged)  # reset merged file

        # When
        solver = ImportImportsSolver()

        # Then
        result = solver.solve_import_conflicts(base, local, remote, merged)
        self.assertFalse(result)
        self.assertTrue(cmp(IS_PATH.format("merged_solved_imports"), merged,
                            shallow=False))  # merged is untouched

    def test_conflict_complex_mixed_section_grouped(self):
        class ImportImportsSolver(ImportsSolver):
            def is_import_line(self, line: str) -> bool:
                return line.startswith("import ")

            def is_allowed_within_import_section(self, line: str) -> bool:
                return line.startswith("# ") or line.isspace()

            def get_import_group(self, imp: str) -> int:
                if len(imp) == 0:
                    return 0
                else:
                    tokens = imp.split()
                    return ord(tokens[1][0])

        # Given files
        base = IS_PATH.format("base")
        local = IS_PATH.format("local")
        remote = IS_PATH.format("remote")
        merged = IS_PATH.format("merged")
        merged_src = IS_PATH.format("merged_src")
        copyfile(merged_src, merged)  # reset merged file

        # When
        solver = ImportImportsSolver()

        # Then
        result = solver.solve_import_conflicts(base, local, remote, merged)
        self.assertFalse(result)
        self.assertTrue(
            cmp(IS_PATH.format("merged_solved_imports_grouped"), merged,
                shallow=False))  # merged is untouched


if __name__ == '__main__':
    unittest.main()
