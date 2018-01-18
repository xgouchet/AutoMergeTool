#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from automergetool.solvers.kotlin_imports import *

KI_PATH = 'tests/data/kotlin_imports/{0}.kt'


class SolverTest(unittest.TestCase):
    def test_is_import(self):
        """Test matching imports"""
        # Given a Kotlin Solver and imports
        solver = KotlinImportSolver()

        path = KI_PATH.format("imports_only")
        with open(path) as f:
            for line in f:
                self.assertTrue(solver.is_import_line(line))

    def test_is_not_import(self):
        """Test non matching imports"""
        # Given a Kotlin Solver and imports
        solver = KotlinImportSolver()

        path = KI_PATH.format("no_imports")
        with open(path) as f:
            for line in f:
                self.assertFalse(solver.is_import_line(line))

    def test_compare_imports(self):
        """Test comparing kotlin imports"""
        # Given a Kotlin Solver
        solver = KotlinImportSolver()
        fake_import = "import java.io.File"
        other_fake_import = "     import      java .\t io.File   ;"

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)
        incompatible = solver.are_imports_incompatible(fake_import, other_fake_import)

        # Then check the comparison
        self.assertTrue(same)
        self.assertFalse(incompatible)

    def test_compare_different_imports(self):
        """Test comparing kotlin imports"""
        # Given a Kotlin Solver
        solver = KotlinImportSolver()
        fake_import = "    import java.util.ArrayList;"
        other_fake_import = "import\t      java \t.util . LinkedList   ;"

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)

        # Then check the comparison
        self.assertFalse(same)

    def test_compare_renamed_imports(self):
        """Test comparing kotlin imports"""
        # Given a Kotlin Solver
        solver = KotlinImportSolver()
        fake_import = "    import java.util.ArrayList as AList"
        other_fake_import = "import        \t java    . util.   ArrayList \tas    AList ; "

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)
        incompatible = solver.are_imports_incompatible(fake_import, other_fake_import)

        # Then check the comparison
        self.assertTrue(same)
        self.assertFalse(incompatible)

    def test_compare_differently_renamed_imports(self):
        """Test comparing kotlin imports"""
        # Given a Kotlin Solver
        solver = KotlinImportSolver()
        fake_import = "import java.lang.annotation.Retention as JRetention"
        other_fake_import = "import     \t java\t.lang.annotation. Retention as JavaRetention "

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)
        incompatible = solver.are_imports_incompatible(fake_import, other_fake_import)

        # Then check the comparison
        self.assertTrue(same)
        self.assertTrue(incompatible)

    def test_compare_different_renamed_imports(self):
        """Test comparing kotlin imports"""
        # Given a Kotlin Solver
        solver = KotlinImportSolver()
        fake_import = "import java.lang.annotation.Retention as JRetention"
        other_fake_import = "    import java.util.ArrayList as AList"

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)

        # Then check the comparison
        self.assertFalse(same)

    def test_compare_samely_renamed_different_imports(self):
        """Test comparing kotlin imports"""
        # Given a Kotlin Solver
        solver = KotlinImportSolver()
        fake_import = "import java.lang.annotation.Retention as JR"
        other_fake_import = "    import java.util.Runnable as JR"

        # When handling the conflict
        with self.assertRaises(RuntimeError):
            same = solver.are_imports_the_same(fake_import, other_fake_import)


    # noinspection PyUnresolvedReferences
    def test_path_arguments_shorts(self):
        # Given
        b = "b"
        l = "l"
        r = "r"
        m = "m"

        # When
        parsed = parse_arguments(['-b', b, '-m', m, '-l', l, '-r', r])

        self.assertEqual(parsed.base, b)
        self.assertEqual(parsed.local, l)
        self.assertEqual(parsed.remote, r)
        self.assertEqual(parsed.merged, m)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_long(self):
        # Given
        b = "b"
        l = "l"
        r = "r"
        m = "m"

        # When
        parsed = parse_arguments(['--base', b, '--merged', m, '--local', l, '--remote', r])

        self.assertEqual(parsed.base, b)
        self.assertEqual(parsed.local, l)
        self.assertEqual(parsed.remote, r)
        self.assertEqual(parsed.merged, m)

    def test_missing_arguments(self):
        b = "b"
        l = "l"
        r = "r"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parse_arguments(['--base', b, '--merged', m, '--remote', r])

    def test_unknown_argument(self):
        b = "b"
        l = "l"
        r = "r"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parse_arguments(
                ['--base', b, '--merged', m, '--local', l, '--remote', r, '--kamoulox', '-p'])



if __name__ == '__main__':
    unittest.main()
