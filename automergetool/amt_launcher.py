#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import subprocess
import sys
from configparser import RawConfigParser
from typing import Optional, Dict, List

SECT_TOOL_FORMAT = 'mergetool "{0}"'
OPT_PATH = 'path'
OPT_CMD = 'cmd'
OPT_EXTENSIONS = 'extensions'
OPT_IGNORED_EXTENSIONS = 'ignoreExtensions'
OPT_TRUST_EXIT_CODE = 'trustExitCode'

CURRENT_FRAME = inspect.getfile(inspect.currentframe())
CURRENT_DIR = os.path.dirname(os.path.abspath(CURRENT_FRAME))
CURRENT_INTERPRETER = sys.executable

KNOWN_PATHS = {  # type: Dict[str, str]
    'java_imports': CURRENT_DIR + '/solvers/java_imports.py',
    'gen_additions': CURRENT_DIR + '/solvers/gen_additions.py',
    'gen_deletions': CURRENT_DIR + '/solvers/gen_deletions.py',
    'gen_debug': CURRENT_DIR + '/solvers/gen_debug.py',
    'gen_simplify': CURRENT_DIR + '/solvers/gen_simplify.py',
    'gen_woven': CURRENT_DIR + '/solvers/gen_woven.py',
    'gen_single_line': CURRENT_DIR + '/solvers/gen_single_line.py'
}

KNOWN_CMDS = {  # type: Dict[str, str]
    # 3rd party solvers (Tested at least once on a Linux Ubuntu Xenial x64 and a Zesty)
    'bc': '"{0}" "$LOCAL" "$REMOTE" "$BASE" '
          '-mergeoutput="$MERGED"',
    'bc3': '"{0}" "$LOCAL" "$REMOTE" "$BASE" '
           '-mergeoutput="$MERGED"',
    'bcompare': '"{0}" "$LOCAL" "$REMOTE" "$BASE" '
                '-mergeoutput="$MERGED"',
    'diffmerge': '"{0}" --merge --result="$MERGED" "$LOCAL" "$BASE" "$REMOTE"',
    'diffuse': '"{0}" "$LOCAL" "$MERGED" "$REMOTE" "$BASE"',
    'ecmerge': '"{0}" "$BASE" "$LOCAL" "$REMOTE" --default --mode=merge3 --to="$MERGED"',
    'kdiff3': '"{0}" --auto '
              '--L1 "$MERGED (Base)"'
              '--L2 "$MERGED (Local)"'
              '--L3 "$MERGED (Remote)"'
              '-o $MERGED $BASE $LOCAL $REMOTE',
    'kompare': '"{0}" "$LOCAL" "$REMOTE"',
    'meld': '"{0}" --output "$MERGED" "$LOCAL" "$BASE" "$REMOTE"',
    'p4merge': '"{0}" "$BASE" "$REMOTE" "$LOCAL" "$MERGED"',
    'tkdiff': '"{0}" -a "$BASE" -o "$MERGED" "$LOCAL" "$REMOTE"',
    'xxdiff': '"{0}" -X --show-merged-pane '
              '-R \'Accel.SaveAsMerged: "Ctrl+S"\' '
              '-R \'Accel.Search: "Ctrl+F"\' '
              '-R \'Accel.SearchForward: "Ctrl+G"\' '
              '--merged-file "$MERGED" "$LOCAL" "$BASE" "$REMOTE"',
    'emerge': '"{0}" '
              '-f emerge-files-with-ancestor-command '
              '"$LOCAL" "$REMOTE" "$BASE" '
              '"$MERGED"',

    # Untested Vim
    'vimdiff': '"{0}" -f -d -c \'4wincmd w | wincmd J\' "$LOCAL" "$BASE" "$REMOTE" "$MERGED"',
    'gvimdiff': '"{0}" -f -d -c \'4wincmd w | wincmd J\' "$LOCAL" "$BASE" "$REMOTE" "$MERGED"',
    'vimdiff2': '"{0}" -f -d -c \'wincmd l\' "$LOCAL" "$MERGED" "$REMOTE"',
    'gvimdiff2': '"{0}" -f -d -c \'wincmd l\' "$LOCAL" "$MERGED" "$REMOTE"',
    'vimdiff3': '"{0}" -f -d -c \'hid | hid | hid\' "$LOCAL" "$REMOTE" "$BASE" "$MERGED"',
    'gvimdiff3': '"{0}" -f -d -c \'hid | hid | hid\' "$LOCAL" "$REMOTE" "$BASE" "$MERGED"',

    # Untested 3rd party solvers, Mac / Windows only
    'araxis': '"{0}" -wait -merge -3 -a1 '
              '"$BASE" "$LOCAL" "$REMOTE" "$MERGED"',
    'deltawalker': '"{0}" "$LOCAL" "$REMOTE" "$BASE" -merged="$MERGED"',

    # Untested 3rd party solvers, Mac only
    'opendiff': '"{0}" "$LOCAL" "$REMOTE" -ancestor "$BASE" -merge "$MERGED" | cat',

    # Untested 3rd party solvers, Windows only
    'codecompare': '"{0}" -MF="$LOCAL" -TF="$REMOTE" -BF="$BASE" -RF="$MERGED"',
    'examdiff': '"{0}" -merge "$LOCAL" "$BASE" "$REMOTE" -o:"$MERGED" -nh',
    'tortoisemerge': '"{0}" '
                     '-base "$BASE" -mine "$LOCAL" '
                     '-theirs "$REMOTE" -merged "$MERGED"',
    'winmerge': '"{0}" -u -e -dl Local -dr Remote '
                '"$LOCAL" "$REMOTE" "$MERGED"',

    # Generic AMT solvers
    'gen_additions': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_deletions': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_debug': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_simplify': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_woven': CURRENT_INTERPRETER + ' {0} -m $MERGED',
    'gen_single_line': CURRENT_INTERPRETER + ' {0} -m $MERGED',

    # Language specific AMT solvers
    'java_imports': CURRENT_INTERPRETER + ' {0} -b $BASE -l $LOCAL -r $REMOTE -m $MERGED'
}

KNOWN_TRUSTS = {  # type: Dict[str, bool]]
    # 3rd party solvers
    'deltawalker': True,
    'emerge': True,
    'diffmerge': True,
    'gvimdiff': True,
    'gvimdiff2': True,
    'gvimdiff3': True,
    'kdiff3': True,
    'tkdiff': True,
    'kompare': True,
    'vimdiff': True,
    'vimdiff2': True,
    'vimdiff3': True,

    # AMT solvers
    'java_imports': True,
    'gen_additions': True,
    'gen_woven': True,
    'gen_debug': True,
    'gen_simplify': True
}

KNOWN_EXTENSIONS = {'java_imports': 'java'}  # type: Dict[str, str]


class ToolsLauncher:
    """
    """

    def __init__(self, config: Optional[RawConfigParser]=None):
        self.config = config

    @staticmethod
    def tool_section_name(tool: str) -> str:
        """
        Generates the mergetool section name for the given tool
        eg : tool_section_name("foo") → [mergetool "foo"]
        """
        return SECT_TOOL_FORMAT.format(tool)

    def get_tool_trust(self, tool: str) -> bool:
        """
        Check whether we should trust the exit code of the given tool
        tool -- the name of the tool
        """
        section = ToolsLauncher.tool_section_name(tool)
        if self.config.has_option(section, OPT_TRUST_EXIT_CODE):
            return self.config.getboolean(section, OPT_TRUST_EXIT_CODE)

        # Known tools path
        if tool in KNOWN_TRUSTS:
            return KNOWN_TRUSTS[tool]

        # Default
        return False

    def get_tool_extensions(self, tool: str) -> Optional[List[str]]:
        """
        Get the extensions list the given tool can work on
        tool -- the name of the tool
        """
        extensions = None

        # Known tools extensions
        if tool in KNOWN_EXTENSIONS:
            extensions = KNOWN_EXTENSIONS[tool]

        # Override in config
        section = ToolsLauncher.tool_section_name(tool)
        if self.config.has_option(section, OPT_EXTENSIONS):
            extensions = self.config.get(section, OPT_EXTENSIONS)

        if extensions:
            return extensions.split(';')
        else:
            return None

    def get_tool_ignored_extensions(self, tool: str) -> Optional[List[str]]:
        """
        Get the extensions list the given tool can work on
        tool -- the name of the tool
        """
        ignored_extensions = None

        # Check in config
        section = ToolsLauncher.tool_section_name(tool)
        if self.config.has_option(section, OPT_IGNORED_EXTENSIONS):
            ignored_extensions = self.config.get(section, OPT_IGNORED_EXTENSIONS)

        if ignored_extensions:
            return ignored_extensions.split(';')
        else:
            return None

    def get_tool_path(self, tool: str) -> str:
        """
        Get the path for the given tool
        tool -- the name of the tool
        """
        section = ToolsLauncher.tool_section_name(tool)
        if self.config.has_option(section, OPT_PATH):
            return self.config.get(section, OPT_PATH)

        # Known tools path
        if tool in KNOWN_PATHS:
            return KNOWN_PATHS[tool]

        # Default
        return tool

    def get_tool_cmd(self, tool: str) -> Optional[str]:
        """
        Get the command line invocation for the givent tool
        tool -- the name of the tool
        config -- the current amt configuration
        """
        section = ToolsLauncher.tool_section_name(tool)
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

    # noinspection PyMethodMayBeStatic
    def invoke(self, cmd: str) -> int:
        """
        Invokes the given command
        :param cmd: the command string
        """
        sanitized_cmd = ToolsLauncher.sanitize_command(cmd)
        return subprocess.call(sanitized_cmd, shell=False)

    @staticmethod
    def sanitize_command(cmd: str) -> list:
        """
        Sanitizes the command into an array of arguments
        :param cmd: the command string
        :return: a list of tokens for the launcher
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


if __name__ == '__main__':
    print("This is just a utility module, not to be launched directly.")
    sys.exit(1)
