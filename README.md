# ArachneMergeTool

## Feature

This program allows you to chain different merge tools when resolving conflicts.

The basic idea is to have simple automatic merging tools that can solve some tedious conflicts solving
(eg: import hell in java classes), and only launch interactive

## Usage

Clone this repository somewhere on your system (eg: `/opt/ArachneMergeTool` or `/usr/local/ArachneMergeTool` on Linux and Mac)

### Git
Update your `.gitconfig` file (either global or per repository) :


    [merge]
    tool = amt
    [mergetool "amt"]
    cmd = python /path/to/ArachneMergeTool.py -b "$BASE" -l "$LOCAL" -r "$REMOTE" -m "$MERGED"

or just type the following in a shell prompt :


    $ git config --global merge.tool amt
    $ git config --global mergetool.extMerge.cmd 'python /path/to/ArachneMergeTool.py -b "$BASE" -l "$LOCAL" -r "$REMOTE" -m "$MERGED"'

### Standalone

Just run the followin, providing the base, local, remote and merged files to the

    $ python /path/to/ArachneMergeTool.py

## Configuration

You can have a global configuration (in ~/.amtconfig) or provide a custom config file in the command
line (with the `-c --config` optional argument).

    [ArachneMergeTool]
    tools = mytool;meld;kdiff;vimdiff

    [mergetool "mytool"]
    cmd = /path/to/mytool --diff $LOCAL $BASE --diff $BASE $REMOTE --diff $LOCAL $MERGED $REMOTE


The most important configuration is the `tools` option which lists the different merge tools in order. If the first listed tool fails, the second one is launched, etc...

For each tool listed in the `tools` option, you can have a `[mergetool "name"]` section¸ which is compatible with `.gitconfig` syntax, with the following options :

 - path : the path to the tool, if it's not already available in PATH
 - cmd : a custom command line invocation. You can use the following variable in the command line : `$BASE`, `$LOCAL`, `$REMOTE` and `$MERGED`
 - trustExitCode : if set to true, this will assume that the exit code reflects the success of the merge. Otherwise, ArachneMergeTool will prompt the user to indicate the success of the resolution after the merge tool has exited.

## Known merge tools

 - meld

Please send us Pull Request or open Issues to let us know what tool you want us to include

## Internal merge tools

ArachneMergeTool comes bundled with a few automated tools that you can use to handle some known and tedious conflicts easily.

 - **MergeJavaImports** : this will handle any conflict within the imports section of your java files

## Caveats

For now, the config file for ArachneMergeTool doesn't support leading whitespaces. Converting to python 3.0 should fix that

## Todo

 - Right now, AMT is written for Python 2.7. A 3.0 compatible version should be written soon
 - For now only meld is recognized as a known merging tool. Others could be included from [Git's mergetools code](https://github.com/git/git/tree/master/mergetools).

## Contribute

If you want to contribute, pull requests are welcome, and you can also report issues.

## See Also

 - [Git Mergetool documentation](https://git-scm.com/docs/git-mergetool)

## License

This program is distributed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0)
