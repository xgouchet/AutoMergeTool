#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
import re
import sys

from automergetool.amt_import_solver import ImportsSolver

IMPORT_WITH_ALIAS_REGEX = re.compile('^\s*import\s+(.*)\s+as\s+([^.;]*)\s*;?\s*')
IMPORT_NO_ALIAS_REGEX = re.compile('^\s*import\s+([^;]+)(\s+as\s+([^;]+))?\s*;?\s*$')
EMPTY_REGEX = re.compile('^[\s\n]*$')

IMPORT_GROUPS_ORDER_ANDROID = [("import android.", 0), ("import com.", 1), ("import junit.", 2),
                               ("import net.", 3), ("import org.", 4), ("import java.", 5),
                               ("import javax.", 6), ("import ", 7), ("import static ", 8)]
IMPORT_GROUPS_ORDER_IJ_IDEA = [("import ", 0), ("import javax.", 1), ("import java.", 2),
                               ("import static ", 3)]

ORDER_ANDROID = "android"
ORDER_IJ_IDEA = "idea"

IMPORT_PRESETS = {
    ORDER_ANDROID: IMPORT_GROUPS_ORDER_ANDROID,
    ORDER_IJ_IDEA: IMPORT_GROUPS_ORDER_IJ_IDEA,
}


class KotlinImportSolver(ImportsSolver):
    # TODO allow custom order configuration
    def __init__(self, order: str = None):
        super().__init__(deep_merge=True)
        if order is not None:
            self.set_import_groups(order)
        else:
            self.import_groups = []

    def is_allowed_within_import_section(self, line: str) -> bool:
        if re.match(EMPTY_REGEX, line):
            return True
        else:
            return False

    def is_import_line(self, line: str) -> bool:
        if re.match(IMPORT_WITH_ALIAS_REGEX, line) is not None:
            return True
        elif re.match(IMPORT_NO_ALIAS_REGEX, line) is not None:
            return True
        else:
            return False

    def set_import_groups(self, preset: str = None):
        """
        Sets the preferred ordering for imports
        preset -- one of "android", "eclipse", "idea"
        """
        if preset is not None:
            if preset in IMPORT_PRESETS:
                groups = IMPORT_PRESETS[preset]
                self.import_groups = sorted(groups, key=lambda grp: len(grp[0]), reverse=True)

    def get_import_group(self, imp: str):
        """
        Returns the group index the imports belongs to
        imp -- the import line
        """
        for group in self.import_groups:
            if imp.startswith(group[0]):
                return group[1]
        return len(self.import_groups)

    def are_imports_the_same(self, imp: str, other_imp: str):
        kimp = KotlinImport(imp)
        other_kimp = KotlinImport(other_imp)
        same_canonical = kimp.canonical == other_kimp.canonical

        if (kimp.alias is not None) and (kimp.alias == other_kimp.alias) and not same_canonical:
            raise RuntimeError("Two imports use the same alias! We can't solve that one!")
        return same_canonical

    def are_imports_incompatible(self, imp: str, other_imp: str):
        kimp = KotlinImport(imp)
        other_kimp = KotlinImport(other_imp)
        if (kimp.alias is None) and (other_kimp.alias is None):
            return False

        same_canonical = kimp.canonical == other_kimp.canonical
        same_alias = (kimp.alias == other_kimp.alias)
        return same_canonical != same_alias


class KotlinImport:
    def __init__(self, line):
        match_with_alias = re.match(IMPORT_WITH_ALIAS_REGEX, line)
        match_without = re.match(IMPORT_NO_ALIAS_REGEX, line)
        if match_with_alias is not None:
            canonical = match_with_alias.group(1)
            alias = match_with_alias.group(2)
        elif match_without is not None:
            canonical = match_without.group(1)
            alias = None
        else:
            raise RuntimeError("Not a kotlin import")

        self.canonical = self.cleanup(canonical)
        if alias is None:
            self.alias = None
        else:
            self.alias = self.cleanup(alias)

    @staticmethod
    def cleanup(source):
        compact = source.replace(" ", "").replace("\t", "")
        return compact


def parse_arguments(args: list) -> Namespace:
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = ArgumentParser(description="A tool to combine multiple merge tools")

    parser.add_argument('-b', '--base', required=True)
    parser.add_argument('-l', '--local', required=True)
    parser.add_argument('-r', '--remote', required=True)
    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument(
        '-o', '--order', choices=[ORDER_IJ_IDEA, ORDER_ANDROID], required=False)

    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])

    solver = KotlinImportSolver(args.order)
    if solver.solve_import_conflicts(args.base, args.local, args.remote, args.merge):
        sys.exit(0)
    else:
        sys.exit(1)
