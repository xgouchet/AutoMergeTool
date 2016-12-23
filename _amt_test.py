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
        args = create_args()

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
        args = create_args()
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
        args = create_args()
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
        args = create_args()
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
        args = create_args()
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
        args = create_args()
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
        args = create_args()
        invocator = Mock(side_effect=lambda cmd: 0)

        # When
        result = merge_with_tool(tool, cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_UNTRUSTED)
        invocator.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tools_all_fail(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_TOOLS, 'foo;bar;baz')
        cfg.add_section('mergetool "foo"')
        cfg.set('mergetool "foo"', OPT_CMD, 'MY_CMD1 $MERGED')
        cfg.set('mergetool "foo"', OPT_TRUST_EXIT_CODE, 'true')
        cfg.add_section('mergetool "bar"')
        cfg.set('mergetool "bar"', OPT_CMD, 'MY_CMD2 --out $MERGED')
        cfg.set('mergetool "bar"', OPT_TRUST_EXIT_CODE, 'true')
        cfg.add_section('mergetool "baz"')
        cfg.set('mergetool "baz"', OPT_CMD, 'MY_CMD3 $BASE $MERGED')
        cfg.set('mergetool "baz"', OPT_TRUST_EXIT_CODE, 'true')
        args = create_args()
        invocator = Mock(side_effect=lambda cmd: 1)

        # When
        result = merge(cfg, args, invocator)

        # Then
        self.assertEqual(result, ERROR_CONFLICTS)
        calls = [
            call('MY_CMD1 ' + args.merged), call('MY_CMD2 --out ' + args.merged),
            call('MY_CMD3 ' + args.base + ' ' + args.merged)
        ]
        invocator.assert_has_calls(calls)

    def test_merge_with_tools_first_succeeds(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_TOOLS, 'foo;bar;baz')
        cfg.add_section('mergetool "foo"')
        cfg.set('mergetool "foo"', OPT_CMD, 'MY_CMD1 $MERGED')
        cfg.set('mergetool "foo"', OPT_TRUST_EXIT_CODE, 'true')
        cfg.add_section('mergetool "bar"')
        cfg.set('mergetool "bar"', OPT_CMD, 'MY_CMD2 --out $MERGED')
        cfg.set('mergetool "bar"', OPT_TRUST_EXIT_CODE, 'true')
        cfg.add_section('mergetool "baz"')
        cfg.set('mergetool "baz"', OPT_CMD, 'MY_CMD3 $BASE $MERGED')
        cfg.set('mergetool "baz"', OPT_TRUST_EXIT_CODE, 'true')
        args = create_args()
        invocator = Mock(side_effect=lambda cmd: 0)

        # When
        result = merge(cfg, args, invocator)

        # Then
        self.assertEqual(result, SUCCESSFUL_MERGE)
        invocator.assert_called_once_with('MY_CMD1 ' + args.merged)

    def test_merge_not_configured(self):
        # Given
        cfg = configparser.ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        invocator = Mock(side_effect=lambda cmd: 1)

        # When
        with self.assertRaises(RuntimeError):
            merge(cfg, args, invocator)

        # Then
        invocator.assert_not_called()


def create_args():
    args = lambda: None
    args.local = "/path/to/blu"
    args.base = "/path/to/plop"
    args.remote = "/path/to/fds"
    args.merged = "/path/to/lol.ext"
    return args


if __name__ == '__main__':
    unittest.main()
