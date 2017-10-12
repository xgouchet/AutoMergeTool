
AutoMergeTool
=============

AutoMergeTool is a tool compatible with git to simplify the process of solving conflicts after a git merge, rebase or cherry-pick.

The code is open source, and available on [GitHub](https://github.com/xgouchet/AutoMergeTool).

Introduction
------------

This program allows you to chain different merge tools when resolving conflicts, instead of just using a single (manual) one.

The basic idea is to have (many) simple automatic merging tools that can solve some tedious conflicts, and only launch
an interactive tool as a last resort solution.

Origin
------

After working for a few years in a large team of developers at [Deezer](http://wwww.deezer.com/), merges and rebases came with a recurring sense of fear. The time spent solving conflicts manually seemed like a lot of waste.

After noticing that many conflicts were actually easily resolvable, but tedious, the idea for this tool sparked.

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   installation
   configuration
   known_merge_tools
   reporting

