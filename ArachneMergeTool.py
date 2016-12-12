#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import inspect
import os
import subprocess
import sys
import configparser

# CONSTANTS
DEFAULT_CONFIG = os.path.expanduser('~/.amtconfig')

SECT_AMT = 'ArachneMergeTool'
OPT_TOOLS = 'tools'
OPT_KEEP_REPORTS = 'keepReport'

SECT_TOOL_FORMAT = 'mergetool "{0}"'
OPT_PATH = 'path'
OPT_CMD = 'cmd'
OPT_TRUST_EXIT_CODE = 'trustExitCode'

CURRENT_FRAME = inspect.getfile(inspect.currentframe())
CURRENT_DIR = os.path.dirname(os.path.abspath(CURRENT_FRAME))

KNOWN_PATHS = {
    'mji': CURRENT_DIR + '/MergeJavaImports.py',
    'mac': CURRENT_DIR + '/MergeAdditionConflicts.py',
    'mwc': CURRENT_DIR + '/MergeWovenConflicts.py'
}
# TODO based on git's internal mergetool code, create defaults for known tools
KNOWN_CMDS = {
    'meld': '{0} --output "$MERGED" "$LOCAL" "$BASE" "$REMOTE"',
    'mji': '{0} -b $BASE -l $LOCAL -r $REMOTE -m $MERGED',
    'mac': '{0} -m $MERGED',
    'mwc': '{0} -m $MERGED'
}
KNOWN_TRUSTS = {'meld': False, 'mji': True, 'mac': True, 'mwc': True}


def parse_arguments():
    """
    Parses the arguments passed on invocation in a dict and return it
    """
    parser = argparse.ArgumentParser(
        description="A tool to combine multiple merge tools")

    parser.add_argument('-b', '--base', required=True)
    parser.add_argument('-l', '--local', required=True)
    parser.add_argument('-r', '--remote', required=True)
    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument('-c', '--config', default=DEFAULT_CONFIG)

    return parser.parse_args()


def read_config(config_path):
    """
    Reads the AMT configuration from the given path
    """
    config = configparser.RawConfigParser()
    config.read(config_path)
    return config


def tool_section_name(tool):
    """
    Generates the mergetool section name for the given tool
    eg : tool_section_name("foo") → [mergetool "foo"]
    """
    return SECT_TOOL_FORMAT.format(tool)


def get_tool_trust(tool, config):
    """
    Check whether we should trust the exit code of the given tool
    tool -- the name of the tool
    config -- the current amt configuration
    """
    section = tool_section_name(tool)
    if config.has_option(section, OPT_TRUST_EXIT_CODE):
        return config.get(section, OPT_TRUST_EXIT_CODE)

    # Known tools path
    if tool in KNOWN_TRUSTS:
        return KNOWN_TRUSTS[tool]

    # Default
    return False


def get_tool_path(tool, config):
    """
    Get the path for the given tool
    tool -- the name of the tool
    config -- the current amt configuration
    """
    section = tool_section_name(tool)
    if config.has_option(section, OPT_PATH):
        return config.get(section, OPT_PATH)

    # Known tools path
    if tool in KNOWN_PATHS:
        return KNOWN_PATHS[tool]

    # Default
    return tool


def get_tool_cmd(tool, config):
    """
    Get the command line invocation for the givent tool
    tool -- the name of the tool
    config -- the current amt configuration
    """
    section = tool_section_name(tool)
    if (config.has_option(section, OPT_CMD)):
        return config.get(section, OPT_CMD)

    path = get_tool_path(tool, config)

    if tool in KNOWN_CMDS:
        cmd = KNOWN_CMDS[tool].format(path)
        if (config.has_section(section)):
            for option in config.options(section):
                if (option == OPT_CMD):
                    pass
                if (option == OPT_PATH):
                    pass
                if (option == OPT_TRUST_EXIT_CODE):
                    pass
                cmd += " --{0} {1}".format(option, config.get(section, option))
        return cmd

    # No Default
    return None


def expand_arguments(cmd, args):
    """
    Expands the named arguments in the command line invocation
    cmd -- the command line invocation
    args -- the arguments with the base, local, remote and merged filenames
    """
    cmd = cmd.replace('$BASE', args.base)
    cmd = cmd.replace('$LOCAL', args.local)
    cmd = cmd.replace('$REMOTE', args.remote)
    cmd = cmd.replace('$MERGED', args.merged)
    return cmd


def merge(config, args):
    """
    Handle the mergetools chain for the given argument
    config -- the current amt configuration
    args -- the arguments with the base, local, remote and merged filenames
    """
    if (not (config.has_option(SECT_AMT, OPT_TOOLS))):
        raise RuntimeError('Missing the {0}.{1} configuration'.format(
            SECT_AMT, OPT_TOOLS))
    tools = config.get(SECT_AMT, OPT_TOOLS).split(';')
    result = 42
    for tool in tools:
        print(" [AMT] → Trying merge with {0}".format(tool))
        # prepare the command line invocation
        print(" [AMT] → Trying merge with {0}".format(tool))
        cmd = get_tool_cmd(tool, config)
        if cmd == None:
            print(" [AMT] — Ignoring tool {0} (unknown tool)".format(tool))
            continue

        cmd = expand_arguments(cmd, args)
        result = subprocess.call(cmd.split(), shell=False)

        trust_exit_code = get_tool_trust(tool, config)
        if trust_exit_code:
            if (result == 0):
                print(" [AMT] ✓ {0} merged successfully".format(tool))
                return 0
            else:
                print(" [AMT] ✗ {0} didn't solve all conflicts".format(tool))
        else:
            # TODO analyse the merged file and look for conflicts
            print(" [AMT] ? {0} returned".format(tool))

    print(" [AMT] ⚑ Sorry, it seems we can't solve it this time")
    return result

def clean_reports(merged):
    """
    Cleans up the reports for the given file
    """
    if config.has_option(SECT_AMT, OPT_KEEP_REPORTS):
        if config.get(SECT_AMT, OPT_KEEP_REPORTS) == "true":
            return
    print (" [AMT] * Cleaning up reports")
    abs_path = os.path.abspath(merged)
    base_name = os.path.basename(merged) + '.'
    dir_path = os.path.dirname(abs_path)
    for file in os.listdir(dir_path):
        if file.startswith(base_name) and file.endswith('-report'):
            os.remove(file)

if __name__ == '__main__':
    print("ArachneMergeTool kickin' in !")
    args = parse_arguments()
    config = read_config(os.path.expanduser(args.config))
    result = merge(config, args)

    if result == 0:
        clean_reports(args.merged)

    sys.exit(result)

