#!/usr/bin/python
# -*- coding: utf-8 -*-

import inspect
import os
import subprocess
import sys

SECT_TOOL_FORMAT = 'mergetool "{0}"'
OPT_PATH = 'path'
OPT_CMD = 'cmd'
OPT_EXTENSIONS = 'extensions'
OPT_TRUST_EXIT_CODE = 'trustExitCode'

CURRENT_FRAME = inspect.getfile(inspect.currentframe())
CURRENT_DIR = os.path.dirname(os.path.abspath(CURRENT_FRAME))
CURRENT_INTERPRETER = sys.executable

KNOWN_PATHS = {
    'java_imports': CURRENT_DIR + '/java_imports.py',
    'gen_additions': CURRENT_DIR + '/gen_additions.py',
    'gen_deletions': CURRENT_DIR + '/gen_deletions.py',
    'gen_debug': CURRENT_DIR + '/gen_debug.py',
    'gen_simplify': CURRENT_DIR + '/gen_simplify.py',
    'gen_woven': CURRENT_DIR + '/gen_woven.py'
}

# TODO based on git's internal mergetool code, create defaults for known tools
KNOWN_CMDS = {
    # 3rd party solvers
    'meld': '{0} --output "$MERGED" "$LOCAL" "$BASE" "$REMOTE"',
    'opendiff': '"{0}" "$LOCAL" "$REMOTE" -ancestor "$BASE" -merge "$MERGED" | cat',
    # AMT solvers
    'java_imports': CURRENT_INTERPRETER + ' {0} -b $BASE -l $LOCAL -r $REMOTE -m $MERGED',
    'gen_additions': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_deletions': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_debug': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_simplify': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_woven': CURRENT_INTERPRETER + ' {0} -m $MERGED'
}

KNOWN_TRUSTS = {
    'java_imports': True,
    'gen_additions': True,
    'gen_woven': True,
    'gen_debug': True,
    'gen_simplify': True
}

KNOWN_EXTENSIONS = {'java_imports': 'java'}


class ToolsLauncher:
    """
    """

    def __init__(self, config=None):
        self.config = config

    def tool_section_name(self, tool):
        """
        Generates the mergetool section name for the given tool
        eg : tool_section_name("foo") → [mergetool "foo"]
        """
        return SECT_TOOL_FORMAT.format(tool)

    def get_tool_trust(self, tool):
        """
        Check whether we should trust the exit code of the given tool
        tool -- the name of the tool
        """
        section = self.tool_section_name(tool)
        if self.config.has_option(section, OPT_TRUST_EXIT_CODE):
            return self.config.getboolean(section, OPT_TRUST_EXIT_CODE)

        # Known tools path
        if tool in KNOWN_TRUSTS:
            return KNOWN_TRUSTS[tool]

        # Default
        return False

    def get_tool_extensions(self, tool):
        """
        Get the extensions list the given tool can work on
        tool -- the name of the tool
        """
        extensions = None

        # Known tools extensions
        if tool in KNOWN_EXTENSIONS:
            extensions = KNOWN_EXTENSIONS[tool]

        # Override in config
        section = self.tool_section_name(tool)
        if self.config.has_option(section, OPT_EXTENSIONS):
            extensions = self.config.get(section, OPT_EXTENSIONS)

        if extensions:
            return extensions.split(';')
        else:
            return None

    def get_tool_path(self, tool):
        """
        Get the path for the given tool
        tool -- the name of the tool
        """
        section = self.tool_section_name(tool)
        if self.config.has_option(section, OPT_PATH):
            return self.config.get(section, OPT_PATH)

        # Known tools path
        if tool in KNOWN_PATHS:
            return KNOWN_PATHS[tool]

        # Default
        return tool

    def get_tool_cmd(self, tool):
        """
        Get the command line invocation for the givent tool
        tool -- the name of the tool
        config -- the current amt configuration
        """
        section = self.tool_section_name(tool)
        if self.config.has_option(section, OPT_CMD):
            return self.config.get(section, OPT_CMD)

        path = self.get_tool_path(tool)

        if tool in KNOWN_CMDS:
            cmd = KNOWN_CMDS[tool].format(path)
            if self.config.has_section(section):
                for option in self.config.options(section):
                    if option == OPT_PATH or option == OPT_TRUST_EXIT_CODE:
                        pass
                    else:
                        cmd += " --{0} {1}".format(option, self.config.get(section, option))
            return cmd

        # No Default
        return None

    def sanitize_command(self, cmd):
        """
        Sanitizes the command into an array of arguments
        :param cmd:
        :return:
        """
        within_quote = False
        within_double_quote = False
        tokens = []
        accumulator = ""
        for c in cmd:
            if c == '"' and not within_quote:
                if within_double_quote:
                    if len(accumulator) > 0:
                        tokens.append(accumulator)
                        accumulator = ""
                    within_double_quote = False
                else:
                    if len(accumulator) == 0:
                        within_double_quote = True
                    else:
                        accumulator += c
            elif c == '\'' and not within_double_quote:
                if within_quote:
                    if len(accumulator) > 0:
                        tokens.append(accumulator)
                        accumulator = ""
                    within_quote = False
                else:
                    if len(accumulator) == 0:
                        within_quote = True
                    else:
                        accumulator += c
            elif (c == ' ' or c == '\t' or c == '\n') and (not within_double_quote) and (
                    not within_quote):
                if len(accumulator) > 0:
                    tokens.append(accumulator)
                    accumulator = ""
            else:
                accumulator += c

        if len(accumulator) > 0:
            tokens.append(accumulator)
        return tokens

    def invoke(self, cmd):
        """
        Invokes the given command
        """
        sanitized_cmd = self.sanitize_command(cmd)
        return subprocess.call(sanitized_cmd, shell=False)
