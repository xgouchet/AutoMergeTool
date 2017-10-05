# AutoMergeTool

> AutoMergeTool is a tool compatible with git to simplify the process of solving conflicts after a git merge, rebase or cherry-pick.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.5-blue.svg)](https://docs.python.org/3/whatsnew/3.5.html)
[![Build Status](https://travis-ci.org/xgouchet/AutoMergeTool.svg?branch=master)](https://travis-ci.org/xgouchet/AutoMergeTool) [![codecov](https://codecov.io/gh/xgouchet/AutoMergeTool/branch/master/graph/badge.svg)](https://codecov.io/gh/xgouchet/AutoMergeTool)

AMT enables you to chain automatic solvers on git conflicts, before openning your preferred manual merge tool (meld, kdiff, winmerge, …). It is currently under active development, and used internally in the Deezer Android team.



## Installation

**TL;DR;** The easiest way to install AMT is to [download](https://github.com/xgouchet/AutoMergeTool/archive/master.zip) or clone the archive somewhere, then include the following inside your `~/.gitconfig` file : 

    [merge]
        tool = amt
        conflictstyle = diff3
    [mergetool "amt"]
        cmd = /path/to/amt.py -b "$BASE" -l "$LOCAL" -r "$REMOTE" -m "$MERGED"
    [amt]
        tools = gen_simplify;gen_woven;gen_additions;gen_deletions;meld

**Prerequisite** : AutoMergeTool requires Python 3.5, and won't work with Python 2.x.

You can also read the documentation for [installation](https://github.com/xgouchet/AutoMergeTool/wiki/Installation) and [configuration](https://github.com/xgouchet/AutoMergeTool/wiki/Configuration) instructions.

## Usage example

Just use it as your default `mergetool`

## Release History

 * This app is currently in alpha version

## Contribute

If you want to contribute, please follow the [Contribution guidelines](CONTRIBUTING.md).

## See Also

 - Contact me on Twitter [@xgouchet](https://twitter.com/xgouchet)
 - [Git Mergetool documentation](https://git-scm.com/docs/git-mergetool)
 - [Git Config documentation](https://git-scm.com/docs/git-config)

## License

This program is distributed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0)

