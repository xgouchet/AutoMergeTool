import argparse
import sys
import re

IMPORT_REGEX = re.compile('^\s*import\s+(static\s+)?(.*)\s*;\s*$')
PACKAGE_REGEX = re.compile('^\s*package\s+[\w][\w\.]+[\w].*$')
EMPTY_REGEX = re.compile('^[\s\n]*$')

CONFLICT_START = "<<<<<<<"
CONFLICT_BASE  = "|||||||"
CONFLICT_SEP   = "======="
CONFLICT_END   = ">>>>>>>"



def parse_arguments():
    parser = argparse.ArgumentParser(description="A tool to combine multiple merge tools")

    parser.add_argument('-b', '--base', required=True)
    parser.add_argument('-l', '--local', required=True)
    parser.add_argument('-r', '--remote', required=True)
    parser.add_argument('-m', '--merged', required=True)

    return parser.parse_args()


def read_imports(filename):
    imports = []
    with open(filename) as f:
        content = f.readlines()
        for line in content:
            if re.match(IMPORT_REGEX, line):
                imports.append(line)
    return sorted(imports)


def get_merge_imports(args):
    imports_base = read_imports(args.base)
    imports_local = read_imports(args.local)
    imports_remote = read_imports(args.remote)
    imports_merged = []

    # find imports still present in both cases
    for imp in imports_base:
        if (imp in imports_local) and (imp in imports_remote):
            imports_merged.append(imp)
            imports_local.remove(imp)
            imports_remote.remove(imp)

    # add imports from local
    for imp in imports_local:
        if (imp not in imports_merged):
            imports_merged.append(imp)

    # add imports from remote
    for imp in imports_remote:
        if (imp not in imports_merged):
            imports_merged.append(imp)

    return sorted(imports_merged)


def write_merged_imports(f, imports):
    previous_tld = ''
    for imp in imports :
        name = re.search(IMPORT_REGEX, imp)
        tld = name.group(2).split('.', 1)[0]
        if not(tld == previous_tld) :
            f.write("\n")
            previous_tld = tld
        f.write(imp)


def apply_imports(merged_filename, imports):

    conflict = False
    conflict_content = ""
    keep_conflict = False
    complete = True

    with open(merged_filename) as f:
        content = f.readlines()
    with open(merged_filename, 'w') as f:
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
                else :
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
    return complete


def has_merged_conflicts(merged_filename):
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
    if not(has_merged_conflicts(args.merged)):
        print ("No java imports conflicts, ignored")
        # do nothing, leave as is
        sys.exit(1)
    merged_imports = get_merge_imports(args)
    if apply_imports(args.merged, merged_imports) :
        sys.exit(0)
    else :
        sys.exit(1)
