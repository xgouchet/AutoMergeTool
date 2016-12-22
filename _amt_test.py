#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import *

from amt import *

FAKE_TOOL = 'blu'
FAKE_TOOL_SECTION = 'mergetool "blu"'


class AMTTest(unittest.TestCase):
    def test_write_section_name(self):
        section = tool_section_name(FAKE_TOOL)
        self.assertEqual(section, FAKE_TOOL_SECTION)

    def test_get_tool_trust_from_config_none(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        trust = get_tool_trust(FAKE_TOOL, cfg)

        # Then
        self.assertFalse(trust)

    def test_get_tool_trust_from_config_overriden_false(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'false')

        # When
        trust = get_tool_trust(FAKE_TOOL, cfg)

        # Then
        self.assertFalse(trust)

    def test_get_tool_trust_from_config_overriden_true(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'true')

        # When
        trust = get_tool_trust(FAKE_TOOL, cfg)

        # Then
        self.assertTrue(trust)

    def test_get_tool_trust_from_config_overriden_not_boolean(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'plop')

        # When
        with self.assertRaises(ValueError):
            trust = get_tool_trust(FAKE_TOOL, cfg)

    def test_get_tool_trust_from_config_known(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        trust = get_tool_trust('gen_debug', cfg)

        # Then
        self.assertTrue(trust)

    def test_get_tool_extensions_none(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        exts = get_tool_extensions(FAKE_TOOL, cfg)

        # Then
        self.assertIsNone(exts)

    def test_get_tool_extensions_override(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_EXTENSIONS, 'a;b;c')

        # When
        exts = get_tool_extensions(FAKE_TOOL, cfg)

        # Then
        self.assertEqual(exts, ['a', 'b', 'c'])

    def test_get_tool_extensions_known(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        exts = get_tool_extensions('java_imports', cfg)

        # Then
        self.assertEqual(exts, ['java'])

    def test_get_tool_path_none(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        path = get_tool_path(FAKE_TOOL, cfg)

        # Then
        self.assertEqual(path, FAKE_TOOL)

    def test_get_tool_path_override(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_PATH, '/path/to/bar')

        # When
        path = get_tool_path(FAKE_TOOL, cfg)

        # Then
        self.assertEqual(path, '/path/to/bar')

    def test_get_tool_path_known(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        path = get_tool_path('gen_debug', cfg)

        # Then
        self.assertEqual(path, KNOWN_PATHS['gen_debug'])

    def test_get_tool_cmd_none(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        cmd = get_tool_cmd(FAKE_TOOL, cfg)

        # Then
        self.assertIsNone(cmd)

    def test_get_tool_cmd_overriden(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_CMD, 'spam')

        # When
        cmd = get_tool_cmd(FAKE_TOOL, cfg)

        # Then
        self.assertEqual(cmd, 'spam')

    def test_get_tool_cmd_known(self):
        # Given
        cfg = configparser.ConfigParser()

        # When
        cmd = get_tool_cmd('gen_debug', cfg)

        # Then
        self.assertEqual(cmd, KNOWN_PATHS['gen_debug'] + ' -m $MERGED')

    def test_get_tool_cmd_known_with_options(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section('mergetool "gen_debug"')
        cfg.set('mergetool "gen_debug"', 'breakfast', 'bacon')

        # When
        cmd = get_tool_cmd('gen_debug', cfg)

        # Then
        self.assertEqual(cmd, KNOWN_PATHS['gen_debug'] + ' -m $MERGED --breakfast bacon')

    def test_expand_arguments(self):
        # Given
        args = lambda: None
        args = self.__create_args()

        # When
        cmd = "foo -from $BASE -to $LOCAL $REMOTE -out $MERGED"
        cmd = expand_arguments(cmd, args)

        # Then
        self.assertEqual(cmd, "foo -from " + args.base + " -to " + args.local + " " + args.remote +
                         " -out " + args.merged)

    def test_merge_with_none(self):
        # Given
        tool = None
        cfg = configparser.ConfigParser()
        args = self.__create_args()
        invocator = Mock(side_effect=Exception('Should not be invoked'))

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_NO_TOOL)

    def test_merge_with_bad_extensions(self):
        # Given
        tool = FAKE_TOOL
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_EXTENSIONS, 'bacon;spam')
        args = self.__create_args()
        invocator = Mock(side_effect=Exception('Should not be invoked'))

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_EXTENSION)

    def test_merge_with_unknoown_tool(self):
        # Given
        tool = FAKE_TOOL
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_EXTENSIONS, 'bacon;ext;spam')
        args = self.__create_args()
        invocator = Mock(side_effect=Exception('Should not be invoked'))

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_UNKNOWN)

    def test_merge_with_tool_success(self):
        # Given
        tool = FAKE_TOOL
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_CMD, 'MY_CMD $MERGED')
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'true')
        args = self.__create_args()
        invocator = Mock(side_effect=lambda cmd: 0)

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, SUCCESSFUL_MERGE)
        invocator.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tool_remaining_conflicts(self):
        # Given
        tool = FAKE_TOOL
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_CMD, 'MY_CMD $MERGED')
        cfg.set(FAKE_TOOL_SECTION, OPT_TRUST_EXIT_CODE, 'true')
        args = self.__create_args()
        invocator = Mock(side_effect=lambda cmd: 666)

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_CONFLICTS)
        invocator.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tool_untrusted(self):
        # Given
        tool = FAKE_TOOL
        cfg = configparser.ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.set(FAKE_TOOL_SECTION, OPT_CMD, 'MY_CMD $MERGED')
        args = self.__create_args()
        invocator = Mock(side_effect=lambda cmd: 0)

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_UNTRUSTED)
        invocator.assert_called_with('MY_CMD ' + args.merged)

    def __create_args(self):
        args = lambda: None
        args.local = "/path/to/blu"
        args.base = "/path/to/plop"
        args.remote = "/path/to/fds"
        args.merged = "/path/to/lol.ext"
        return args


if __name__ == '__main__':
    unittest.main()
