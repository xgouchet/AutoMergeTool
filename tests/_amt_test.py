#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from configparser import ConfigParser
from unittest.mock import *

import tempfile

from automergetool.amt import *
from automergetool.amt_utils import *

FAKE_TOOL = 'blu'
FAKE_TOOL_SECTION = 'mergetool "blu"'


class AMTTest(unittest.TestCase):
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
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher = Mock()
        analyser = Mock()

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_NO_TOOL)
        launcher.assert_not_called()

    def test_merge_with_bad_extensions(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {'get_tool_extensions.return_value': 'bacon;spam'}
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_EXTENSION)

    def test_merge_with_ignored_extensions(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': 'bacon;spam;ext'
        }
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_EXTENSION)

    def test_merge_with_unknown_tool(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_extensions.return_value': 'bacon;ext;spam',
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.return_value': None
        }
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_UNKNOWN)

    def test_merge_with_tool_success(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_trust.return_value': True,
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.return_value': 'MY_CMD $MERGED',
            'invoke.return_value': 0
        }
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, SUCCESS)
        launcher.invoke.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tool_remaining_conflicts(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(FAKE_TOOL_SECTION)
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_trust.return_value': True,
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.return_value': 'MY_CMD $MERGED',
            'invoke.return_value': 6
        }
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_CONFLICTS)
        launcher.invoke.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tool_untrusted_solved(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_trust.return_value': False,
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.return_value': 'MY_CMD $MERGED',
            'invoke.return_value': 0
        }
        launcher = Mock(**launcher_args)
        analyser_args = {'has_remaining_conflicts.return_value': False}
        analyser = Mock(**analyser_args)

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, SUCCESS)
        launcher.invoke.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tool_untrusted_unsolved(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_trust.return_value': False,
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.return_value': 'MY_CMD $MERGED',
            'invoke.return_value': 0
        }
        launcher = Mock(**launcher_args)
        analyser_args = {'has_remaining_conflicts.return_value': True}
        analyser = Mock(**analyser_args)

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_CONFLICTS)
        launcher.invoke.assert_called_with('MY_CMD ' + args.merged)


    def test_merge_with_tool_failing(self):
        # Given
        tool = FAKE_TOOL
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher_args = {
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.return_value': 'MY_CMD $MERGED',
            'invoke.side_effect': Exception("Oops"),
            'get_tool_trust.return_value': True
        }
        launcher = Mock(**launcher_args)
        analyser_args = {'has_remaining_conflicts.return_value': True}
        analyser = Mock(**analyser_args)

        # When
        result = merge_with_tool(tool, cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_INVOCATION)
        launcher.invoke.assert_called_with('MY_CMD ' + args.merged)

    def test_merge_with_tools_all_fail(self):
        # Given
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_TOOLS, 'foo;bar;baz')
        args = create_args()
        launcher_args = {
            'get_tool_trust.return_value': True,
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.side_effect':
            ['MY_CMD1 $MERGED', 'MY_CMD2 --out $MERGED', 'MY_CMD3 $BASE $MERGED'],
            'invoke.return_value': 1
        }
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge(cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_CONFLICTS)
        calls = [
            call('MY_CMD1 ' + args.merged), call('MY_CMD2 --out ' + args.merged),
            call('MY_CMD3 ' + args.base + ' ' + args.merged)
        ]
        launcher.invoke.assert_has_calls(calls)

    def test_merge_with_tools_first_succeeds(self):
        # Given
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_TOOLS, 'foo;bar;baz')
        args = create_args()
        launcher_args = {
            'get_tool_trust.return_value': True,
            'get_tool_extensions.return_value': None,
            'get_tool_ignored_extensions.return_value': None,
            'get_tool_cmd.side_effect':
                ['MY_CMD1 $MERGED', 'MY_CMD2 --out $MERGED', 'MY_CMD3 $BASE $MERGED'],
            'invoke.return_value': 0
        }
        launcher = Mock(**launcher_args)
        analyser = Mock()

        # When
        result = merge(cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, SUCCESS)
        launcher.invoke.assert_called_once_with('MY_CMD1 ' + args.merged)

    def test_merge_with_tools_empty(self):
        # Given
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_TOOLS, '')
        args = create_args()
        launcher = Mock()
        analyser = Mock()

        # When
        result = merge(cfg, args, launcher, analyser)

        # Then
        self.assertEqual(result, ERROR_NO_TOOL)

    def test_merge_not_configured(self):
        # Given
        cfg = ConfigParser()
        cfg.add_section(SECT_AMT)
        cfg.set(SECT_AMT, OPT_VERBOSE, 'true')
        args = create_args()
        launcher = Mock(side_effect=lambda cmd: 1)
        analyser = Mock()

        # When
        with self.assertRaises(RuntimeError):
            merge(cfg, args, launcher, analyser)

        # Then
        launcher.assert_not_called()

    def test_find_local_config_not_a_git_folder(self):
        # Given
        path = '/foo/bar/spam'

        # When
        config = find_local_config_path(path)

        # Then
        self.assertEqual(config, None)

    def test_find_local_config_not_a_real_folder(self):
        # Given
        path = '/foo/bar/spam'

        # When
        config = find_local_config_path(path)

        # Then
        self.assertEqual(config, None)

    def test_find_local_config_in_current_repo_git_folder(self):
        # Given
        parent = tempfile.mkdtemp()
        gitDir = parent + os.sep + ".git"
        os.mkdir(gitDir)
        configFile = gitDir + os.sep + "config"
        open(configFile, 'a').close()

        path = parent + os.sep + "fakedir" + os.sep + "fakefile"

        # When
        config = find_local_config_path(path)

        # Then
        self.assertEqual(config, configFile)


    def test_no_local_config_in_current_repo_git_folder(self):
        # Given
        parent = tempfile.mkdtemp()
        gitDir = parent + os.sep + ".git"
        os.mkdir(gitDir)
        indexFile = gitDir + os.sep + "index"
        open(indexFile, 'a').close()

        path = parent + os.sep + "fakedir" + os.sep + "fakefile"

        # When
        config = find_local_config_path(path)

        # Then
        self.assertEqual(config, None)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_shorts(self):
        # Given
        b = "b"
        l = "l"
        r = "r"
        m = "m"
        base_path = os.path.abspath(os.getcwd())

        # When
        parsed = parse_arguments(['-b', b, '-m', m, '-l', l, '-r', r])

        self.assertEqual(parsed.base, base_path + os.sep + b)
        self.assertEqual(parsed.local, base_path + os.sep + l)
        self.assertEqual(parsed.remote, base_path + os.sep + r)
        self.assertEqual(parsed.merged, base_path + os.sep + m)

    # noinspection PyUnresolvedReferences
    def test_path_arguments_long(self):
        # Given
        b = "b"
        l = "l"
        r = "r"
        m = "m"
        base_path = os.path.abspath(os.getcwd())

        # When
        parsed = parse_arguments(['--base', b, '--merged', m, '--local', l, '--remote', r])

        self.assertEqual(parsed.base, base_path + os.sep + b)
        self.assertEqual(parsed.local, base_path + os.sep + l)
        self.assertEqual(parsed.remote, base_path + os.sep + r)
        self.assertEqual(parsed.merged, base_path + os.sep + m)

    def test_missing_arguments(self):
        b = "b"
        l = "l"
        r = "r"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parse_arguments(['--base', b, '--merged', m, '--remote', r])

    def test_unknown_argument(self):
        b = "b"
        l = "l"
        r = "r"
        m = "m"

        with self.assertRaises(SystemExit) as context:
            parse_arguments(
                ['--base', b, '--merged', m, '--local', l, '--remote', r, '--kamoulox', '-p'])


def create_args():
    args = lambda: None
    args.local = "/path/to/blu"
    args.base = "/path/to/plop"
    args.remote = "/path/to/fds"
    args.merged = "/path/to/lol.ext"
    return args


if __name__ == '__main__':
    unittest.main()
