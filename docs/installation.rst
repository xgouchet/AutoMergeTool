Installation
------------

Requirements
~~~~~~~~~~~~

**AutoMergeTool** requires Python 3.5. Make sure that your computer uses
that version, or higher.

Install using ``pip`` / ``easy_install``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**AutoMergeTool** is distributed on the PyPi repository, meaning you can
install it easily using **pip**:

.. code:: bash

    $ pip install automergetool

… or using **easy\_install**:

.. code:: bash

    $ easy_install automergetool

Configure git
~~~~~~~~~~~~~

Update your git config, either the global ``~/.gitconfig`` or the
``.git/config`` file in a specific repository :

::

    [merge]
        tool = amt
        conflictstyle = diff3
    [mergetool "amt"]
        cmd = amt -b "$BASE" -l "$LOCAL" -r "$REMOTE" -m "$MERGED"

Alternatively, you can just type the following in a shell prompt (ommit
the ``--global`` to only set the configuration for the current
repository) :

::

    $ git config --global merge.tool amt
    $ git config --global merge.conflictstyle diff3
    $ git config --global mergetool.amt.cmd 'amt -b "$BASE" -l "$LOCAL" -r "$REMOTE" -m "$MERGED"'

Minimal AutoMergeTool configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**AutoMergeTool** requires a minimal configuration. The most basic yet
important one is to set the ``amt.tools`` option in your git config.

::

    [amt]
        tools = gen_simplify;gen_additions;meld
        

Alternatively, you can just type the following in a shell prompt (ommit
the ``--global`` to only set the configuration for the current
repository) :

::

    $ git config --global amt.tools gen_simplify;gen_additions;gen_deletions;meld

The above config will launch the ``gen_simplify``, then
``gen_additions`` tool to solve any conflicted file. If neither of those
solve all conflicts, then the manual tool (here, ``meld``) will be
launched.

You can read the `configuration <configuration>`__ page for more details
on the configuration, and the `Known Merge Tools <known_merge_tools>`__
page for a list of available solvers.

Using AutoMergeTool
~~~~~~~~~~~~~~~~~~~

Now that AutoMergeTool is configured, whenever you get a merge, rebase
or cherry-pick conflict, you can use the following line to automatically
solves conflicts.

.. code:: bash

    $ git mergetool

Note that if you kept another tool as your main ``mergetool``, you can
run **AutoMergeTool** with:

.. code:: bash

    $ git mergetool --tool=amt

--------------

*For more information, read the `configuration page <configuration>`__,
or see the official `Git Mergetool
documentation <https://git-scm.com/docs/git-mergetool>`__*
