#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from automergetool.solvers.java_imports import *


class SolverTest(unittest.TestCase):
    def test_compare_imports(self):
        """Test comparing java imports"""
        # Given a Java Solver
        solver = JavaImportSolver()
        fake_import = "import java.util.ArrayList;"
        other_fake_import = "     import      java.util.ArrayList   ;"

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)
        equal = solver.are_imports_equals(fake_import, other_fake_import)

        # Then check the comparison
        self.assertTrue(same)
        self.assertTrue(equal)

    def test_compare_different_imports(self):
        """Test comparing java imports"""
        # Given a Java Solver
        solver = JavaImportSolver()
        fake_import = "    import java.util.ArrayList;"
        other_fake_import = "import\t      java \t.util . LinkedList   ;"

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)

        # Then check the comparison
        self.assertFalse(same)

    def test_compare_static_imports(self):
        """Test comparing java imports"""
        # Given a Java Solver
        solver = JavaImportSolver()
        fake_import = "import static java.util.Collections.emptyList;"
        other_fake_import = "import     \tstatic   \t java    . util.   Collections.     emptyList ; "

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)
        equal = solver.are_imports_equals(fake_import, other_fake_import)

        # Then check the comparison
        self.assertTrue(same)
        self.assertTrue(equal)

    def test_compare_different_static_imports(self):
        """Test comparing java imports"""
        # Given a Java Solver
        solver = JavaImportSolver()
        fake_import = "import static java.util.Collections.emptyList;"
        other_fake_import = " import     \tstatic   \t java    . util.   Collections. \t    singletonList ; "

        # When handling the conflict
        same = solver.are_imports_the_same(fake_import, other_fake_import)

        # Then check the comparison
        self.assertFalse(same)


if __name__ == '__main__':
    unittest.main()
