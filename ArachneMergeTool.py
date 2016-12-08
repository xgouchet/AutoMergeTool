#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import inspect
import os
import subprocess
import sys
import configparser

# CONSTANTS
DEFAULT_CONFIG = '~/.amtconfig'

SECT_AMT = 'ArachneMergeTool'
OPT_TOOLS = 'tools'

SECT_TOOL_FORMAT = 'mergetool "{0}"'
OPT_PATH = 'path'
OPT_CMD = 'cmd'
OPT_TRUST_EXIT_CODE = 'trustExitCode'

CURRENT_FRAME = inspect.getfile(inspect.currentframe())
CURRENT_DIR = os.path.dirname(os.path.abspath(CURRENT_FRAME))

# TODO based on git's internal mergetool code, create defaults for known tools
KNOWN_PATHS = {'mji': CURRENT_DIR + '/MergeJavaImports.py'}
KNOWN_CMDS = {
    'meld': '{0} --output "$MERGED" "$LOCAL" "$BASE" "$REMOTE" ',
    'mji': '{0} -b $BASE -l $LOCAL -r $REMOTE -m $MERGED '
}
KNOWN_TRUSTS = {
    'meld': False,
    'mji': True,
}


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A tool to combine multiple merge tools")

    parser.add_argument('-b', '--base', required=True)
    parser.add_argument('-l', '--local', required=True)
    parser.add_argument('-r', '--remote', required=True)
    parser.add_argument('-m', '--merged', required=True)
    parser.add_argument('-c', '--config', default=DEFAULT_CONFIG)

    return parser.parse_args()


def read_config(config_path):
    config = configparser.RawConfigParser()
    config.read(config_path)
    return config


def tool_section_name(tool):
    return SECT_TOOL_FORMAT.format(tool)


def get_tool_trust(tool, config):
    section = tool_section_name(tool)
    if config.has_option(section, OPT_TRUST_EXIT_CODE):
        return config.get(section, OPT_TRUST_EXIT_CODE)

    # Known tools path
    if tool in KNOWN_TRUSTS:
        return KNOWN_TRUSTS[tool]

    # Default
    return False


def get_tool_path(tool, config):
    section = tool_section_name(tool)
    if config.has_option(section, OPT_PATH):
        return config.get(section, OPT_PATH)

    # Known tools path
    if tool in KNOWN_PATHS:
        return KNOWN_PATHS[tool]

    # Default
    return tool


def get_tool_cmd(tool, config):
    section = tool_section_name(tool)
    if (config.has_option(section, OPT_CMD)):
        return config.get(section, OPT_CMD)

    path = get_tool_path(tool, config)

    if tool in KNOWN_CMDS:
        cmd = KNOWN_CMDS[tool].format(path)
        for option in config.options(section):
            if (option == OPT_CMD):
                pass
            if (option == OPT_PATH):
                pass
            # print (option)
            cmd += "--{0} {1}".format(option, config.get(section, option))
        return cmd

    # No Default
    print("Unknown tool {0}".format(tool))
    sys.exit(1)


def expand_arguments(cmd, args):
    cmd = cmd.replace('$BASE', args.base)
    cmd = cmd.replace('$LOCAL', args.local)
    cmd = cmd.replace('$REMOTE', args.remote)
    cmd = cmd.replace('$MERGED', args.merged)
    return cmd


def merge(config, args):
    if (not (config.has_option(SECT_AMT, OPT_TOOLS))):
        raise RuntimeError('Missing the {0}.{1} configuration'.format(
            SECT_AMT, OPT_TOOLS))
    tools = config.get(SECT_AMT, OPT_TOOLS).split(';')
    result = 42
    for tool in tools:
        print(" [AMT] → Trying merge with {0}".format(tool))
        # TODO handle the trustExitCode option
        trust_exit_code = True
        cmd = get_tool_cmd(tool, config)
        cmd = expand_arguments(cmd, args)
        #print ("$ {0}".format(cmd))
        result = subprocess.call(cmd.split(), shell=False)
        #print ("Result == " + str(result))
        if trust_exit_code:
            if (result == 0):
                print(" [AMT] ✓ {0} merged successfully".format(tool))
                return 0
            else:
                print(" [AMT] ✗ {0} didn't solve all conflicts".format(tool))
        else:
            # TODO analyse the merged file and look for conflicts
            return 0
    return result


if __name__ == '__main__':
    print("ArachneMergeTool kickin' in !")
    args = parse_arguments()
    config = read_config(os.path.expanduser(args.config))
    result = merge(config, args)
    # print("Exit Code : {0}".format(result))
    sys.exit(result)
