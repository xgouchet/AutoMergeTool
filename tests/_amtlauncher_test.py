#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import unittest

from amtlauncher import *

FAKE_TOOL = 'blu'
FAKE_TOOL_SECTION = 'mergetool "blu"'


class ToolsLauncherTest(unittest.TestCase):
    def test_write_section_name(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        section = launcher.tool_section_name(FAKE_TOOL)

        # Then
        self.assertEqual(section, FAKE_TOOL_SECTION)

    def test_get_tool_trust_from_config_none(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        trust = launcher.get_tool_trust(FAKE_TOOL)

        # Then
        self.assertFalse(trust)

    def test_get_tool_trust_from_config_overriden_false(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'false')
        launcher = ToolsLauncher(cfg)

        # When
        trust = launcher.get_tool_trust(FAKE_TOOL)

        # Then
        self.assertFalse(trust)

    def test_get_tool_trust_from_config_overriden_true(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'true')
        launcher = ToolsLauncher(cfg)

        # When
        trust = launcher.get_tool_trust(FAKE_TOOL)

        # Then
        self.assertTrue(trust)

    def test_get_tool_trust_from_config_overriden_not_boolean(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'plop')
        launcher = ToolsLauncher(cfg)

        # When
        with self.assertRaises(ValueError):
            trust = launcher.get_tool_trust(FAKE_TOOL)

    def test_get_tool_trust_from_config_known(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        trust = launcher.get_tool_trust('gen_debug')

        # Then
        self.assertTrue(trust)

    def test_get_tool_extensions_none(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        exts = launcher.get_tool_extensions(FAKE_TOOL)

        # Then
        self.assertIsNone(exts)

    def test_get_tool_extensions_override(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_EXTENSIONS, 'a;b;c')
        launcher = ToolsLauncher(cfg)

        # When
        exts = launcher.get_tool_extensions(FAKE_TOOL)

        # Then
        self.assertEqual(exts, ['a', 'b', 'c'])

    def test_get_tool_extensions_known(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        exts = launcher.get_tool_extensions('java_imports')

        # Then
        self.assertEqual(exts, ['java'])

    def test_get_tool_ignored_extensions_none(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        exts = launcher.get_tool_ignored_extensions(FAKE_TOOL)

        # Then
        self.assertIsNone(exts)

    def test_get_tool_ignored_extensions_override(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_IGNORED_EXTENSIONS, 'a;b;c')
        launcher = ToolsLauncher(cfg)

        # When
        exts = launcher.get_tool_ignored_extensions(FAKE_TOOL)

        # Then
        self.assertEqual(exts, ['a', 'b', 'c'])

    def test_get_tool_path_none(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        path = launcher.get_tool_path(FAKE_TOOL)

        # Then
        self.assertEqual(path, FAKE_TOOL)

    def test_get_tool_path_override(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_PATH, '/path/to/bar')
        launcher = ToolsLauncher(cfg)

        # When
        path = launcher.get_tool_path(FAKE_TOOL)

        # Then
        self.assertEqual(path, '/path/to/bar')

    def test_get_tool_path_known(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        path = launcher.get_tool_path('gen_debug')

        # Then
        self.assertEqual(path, KNOWN_PATHS['gen_debug'])

    def test_get_tool_cmd_none(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)

        # When
        cmd = launcher.get_tool_cmd(FAKE_TOOL)

        # Then
        self.assertIsNone(cmd)

    def test_get_tool_cmd_overriden(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_CMD, 'spam')
        launcher = ToolsLauncher(cfg)

        # When
        cmd = launcher.get_tool_cmd(FAKE_TOOL)

        # Then
        self.assertEqual(cmd, 'spam')

    def test_get_tool_cmd_known(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)
        interpreter = sys.executable

        # When
        cmd = launcher.get_tool_cmd('gen_debug')

        # Then
        self.assertEqual(cmd, interpreter + ' ' + KNOWN_PATHS['gen_debug'] + ' -m $MERGED')

    def test_get_tool_cmd_known_with_options(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg.add_section('mergetool "gen_debug"')
        cfg.set('mergetool "gen_debug"', 'breakfast', 'bacon')
        cfg.set('mergetool "gen_debug"', 'path', '/toto')
        cfg.set('mergetool "gen_debug"', 'trustExitCode', 'false')
        launcher = ToolsLauncher(cfg)
        interpreter = sys.executable

        # When
        cmd = launcher.get_tool_cmd('gen_debug')

        # Then
        self.assertEqual(cmd, interpreter + ' /toto -m $MERGED --breakfast bacon')

    def test_sanitize_command_simple(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)
        cmd = "foo -o /dev/null/base /dev/null/merged"

        # When
        tokens = launcher.sanitize_command(cmd)

        # Then
        self.assertEqual(tokens, ['foo', '-o', '/dev/null/base', '/dev/null/merged'])

    def test_sanitize_command_with_whitespaces(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)
        cmd = "foo -o  \n  /dev/null/base \t\t /dev/null/merged"

        # When
        tokens = launcher.sanitize_command(cmd)

        # Then
        self.assertEqual(tokens, ['foo', '-o', '/dev/null/base', '/dev/null/merged'])

    def test_sanitize_command_with_quotes(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)
        cmd = "foo -o '/dev/null/base with space' '/dev/null/mergedwith\"e'"

        # When
        tokens = launcher.sanitize_command(cmd)

        # Then
        self.assertEqual(tokens,
                         ['foo', '-o', '/dev/null/base with space', '/dev/null/mergedwith\"e'])

    def test_sanitize_command_with_double_quotes(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)
        cmd = 'foo -o "/dev/null/base with space" "/dev/null/mergedwith\'e"'

        # When
        tokens = launcher.sanitize_command(cmd)

        # Then
        self.assertEqual(tokens,
                         ['foo', '-o', '/dev/null/base with space', '/dev/null/mergedwith\'e'])

    def test_sanitize_command_weird_syntax(self):
        # Given
        cfg = configparser.ConfigParser()
        launcher = ToolsLauncher(cfg)
        cmd = 'foo -o="/dev/null/base" -p=\'/dev/null/merged\''

        # When
        tokens = launcher.sanitize_command(cmd)

        # Then
        self.assertEqual(tokens, ['foo', '-o="/dev/null/base"', '-p=\'/dev/null/merged\''])


if __name__ == '__main__':
    unittest.main()
