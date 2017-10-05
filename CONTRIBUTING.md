# Contribute

## Report Issues

This toolset is still in active development, and although we use dogfooding to make sure we make it as stable and efficient as possible, some issues can still occur.

If you have an error reported while running this tool, please [Report an issue](https://github.com/xgouchet/ArachneMergeTool/issues/new?title=Tool%20Error&labels=tool) including :

 - the exact error message reported
 - your git configuration (`~/.gitconfig` and your repository's `.git/config`)

If you find that a conflict was wrongly resolved, please [Report an issue](https://github.com/xgouchet/ArachneMergeTool/issues/new?title=Conflict%20Error&labels=conflict) including :

 - the different [tools reports](Reporting) if any (use the `solved` or `full` reports mode)
 - the expected resolution
 - your git configuration (`~/.gitconfig` and your repository's `.git/config`)

## Feature Requests

If you use this toolset, and have ideas on how to make it even more usefull, please let us know in a
[Feature request](https://github.com/xgouchet/ArachneMergeTool/issues/new?title=Feature%20Request&labels=enhancement).

## Pull Requests

[Pull Requests](https://github.com/xgouchet/ArachneMergeTool/pulls) are more than welcome.

Before submitting a Pull Request, please make sure that your modifications follow these guidelines :

 - Python code must be properly formated (use the [YAPF](https://github.com/google/yapf) formatter with `pep8` style)
 - New automated solvers must be crossplatform
 - Language specific solver must be prefixed with the name of the language (eg: `java_imports.py`). Make sure that you also fill the `KNOWN_EXTENSIONS` dict in `amt.py`
 - Generic solver must be preficed with `gen_` (eg : `gen_woven.py`)
 - Methods / Classes should have docstrings, and if possible unit tests
 - Commit message must be [properly formatted](http://chris.beams.io/posts/git-commit/)

## Writing a new solver

New solvers can be easily written in python by duplicating the `template/gen_solver.py` and filling in the blanks.

But python is not required so you can write new tools in any language you want, as long as it's crossplatform.


