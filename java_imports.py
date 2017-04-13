#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import re

IMPORT_REGEX = re.compile('^\s*import\s+(static\s+)?(.*)\s*;\s*$')
PACKAGE_REGEX = re.compile('^\s*package\s+[\w][\w\.]+[\w].*$')
EMPTY_REGEX = re.compile('^[\s\n]*$')

CONFLICT_START = "<<<<<<<"
CONFLICT_BASE = "|||||||"
CONFLICT_SEP = "======="
CONFLICT_END = ">>>>>>>"

IMPORT_GROUPS = []

IMPORT_GROUPS_ANDROID = [("import android.", 0), ("import com.", 1), ("import junit.", 2),
                         ("import net.", 3), ("import org.", 4), ("import java.", 5),
                         ("import javax.", 6), ("import ", 7), ("import static ", 8)]
IMPORT_GROUPS_IJ_IDEA = [("import ", 0), ("import javax.", 1), ("import java.", 2),
                         ("import static ", 3)]
IMPORT_GROUPS_ECLIPSE = [("import static ", 0), ("import java.", 1), ("import javax.", 2),
                         ("import org.", 3), ("import com.", 4), ("import ", 5)]

ORDER_ANDROID = "android"
ORDER_IJ_IDEA = "idea"
ORDER_ECLIPSE = "eclipse"

IMPORT_PRESETS = {
    ORDER_ANDROID: IMPORT_GROUPS_ANDROID,
    ORDER_IJ_IDEA: IMPORT_GROUPS_IJ_IDEA,
    ORDER_ECLIPSE: IMPORT_GROUPS_ECLIPSE,
}


def parse_arguments():
    """Parses the arguments passed on invocation in a dict and return it"""
    parser = argparse.ArgumentParser(description="A tool to combine multiple merge tools")

    parser.add_argument('-b', '--base', required=True)
    parser.add_argument('-l', '--local', required=True)
    parser.add_argument('-r', '--remote', required=True)
    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument(
        '-o', '--order', choices=[ORDER_ECLIPSE, ORDER_IJ_IDEA, ORDER_ANDROID], required=False)
    parser.add_argument('-c', '--customorder', required=False)

    return parser.parse_args()


def read_imports(filename):
    """
    Reads all non commented imports from the given file and return them in a list
    filename -- the path to the file to read
    """
    imports = []
    with open(filename) as f:
        content = f.readlines()
        for line in content:
            if re.match(IMPORT_REGEX, line):
                imports.append(line)
    return sorted(imports)


def get_merge_imports(base_file, local_file, remote_file):
    """
    Resolve the imports that should appear in the merged file
    base_file -- the path to the base file
    local_file -- the path to the local file
    remote_file -- the path to the remote file
    """
    imports_base = read_imports(base_file)
    imports_local = read_imports(local_file)
    imports_remote = read_imports(remote_file)
    imports_merged = []

    # find imports still present in both cases
    for imp in imports_base:
        if (imp in imports_local) and (imp in imports_remote):
            imports_merged.append(imp)
            imports_local.remove(imp)
            imports_remote.remove(imp)
    # add imports from local
    for imp in imports_local:
        if ((imp not in imports_merged) and (imp not in imports_base)):
            imports_merged.append(imp)

    # add imports from remote
    for imp in imports_remote:
        if ((imp not in imports_merged) and (imp not in imports_base)):
            imports_merged.append(imp)
    return imports_merged


# TODO add the possibility to define ordering customs from a config file
def set_import_groups(preset=None):
    """
    Sets the prefered ordering for imports
    preset -- one of "android", "eclipse", "idea"
    """
    global IMPORT_GROUPS
    if (preset != None):
        if preset in IMPORT_PRESETS:
            IMPORT_GROUPS = sorted(
                IMPORT_PRESETS[preset], key=lambda grp: len(grp[0]), reverse=True)


def get_import_group(imp):
    """
    Returns the group index the imports belongs to
    imp -- the import line
    """
    for group in IMPORT_GROUPS:
        if (imp.startswith(group[0])):
            return group[1]
    return len(IMPORT_GROUPS)


def write_merged_imports(f, imports):
    """
    Sorts and write the given imports to the file, adding a blank line between
    each group
    f -- the file object (needs write permission)
    imports -- the list of imports
    """
    sorted_imports = sorted(sorted(imports), key=lambda i: get_import_group(i))
    previous_group = -1
    for imp in sorted_imports:
        group = get_import_group(imp)
        if not (group == previous_group):
            f.write("\n")
            previous_group = group
        f.write(imp)


def apply_imports(filename, imports):
    """
    Rewrite the given file, replacing the imports by the list given in parameters
    filename -- path to the file to rewrite
    imports -- the list of imports to use
    """
    conflict = False
    conflict_content = ""
    keep_conflict = False
    complete = True

    # First read the original content
    with open(filename) as f:
        content = f.readlines()
    # then rewrite the file
    with open(filename, 'w') as f:
        for line in content:
            if (conflict):
                conflict_content += line
                if line.startswith(CONFLICT_END):
                    conflict = False
                    if keep_conflict:
                        complete = False
                        f.write(conflict_content)
                elif line.startswith(CONFLICT_SEP) or line.startswith(CONFLICT_BASE):
                    continue
                elif re.match(IMPORT_REGEX, line):
                    continue
                elif re.match(EMPTY_REGEX, line):
                    continue
                else:
                    keep_conflict = True
            elif re.match(IMPORT_REGEX, line):
                continue
            elif re.match(PACKAGE_REGEX, line):
                f.write(line)
                write_merged_imports(f, imports)
            elif line.startswith(CONFLICT_START):
                conflict = True
                keep_conflict = False
                conflict_content = line
            else:
                f.write(line)
    f.close()
    return complete


def has_merged_conflicts(merged_filename):
    """
    Check if the current file has any conflicts in the imports section
    """
    conflict = False
    with open(merged_filename) as f:
        for line in f:
            if (conflict):
                if line.startswith(CONFLICT_END):
                    conflict = False
                elif line.startswith(CONFLICT_SEP) or line.startswith(CONFLICT_BASE):
                    continue
                elif re.match(IMPORT_REGEX, line):
                    return True
            elif line.startswith(CONFLICT_START):
                conflict = True
    return False


if __name__ == '__main__':
    args = parse_arguments()
    if not (has_merged_conflicts(args.merged)):
        print("No java imports conflicts, ignored")
        sys.exit(1)
    set_import_groups(args.order)
    merged_imports = get_merge_imports(args.base, args.local, args.remote)
    if apply_imports(args.merged, merged_imports):
        sys.exit(0)
    else:
        sys.exit(1)
