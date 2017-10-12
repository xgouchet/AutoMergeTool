Configuration
-------------

Please note that every configuration described here can be added either
to your global ``~/.gitconfig`` file or to per-project ``.git/config``
files.

AutoMergeTool
~~~~~~~~~~~~~

Conflict solvers
^^^^^^^^^^^^^^^^

The basic AutoMergeTool configuration you need is set the list of
solvers which will be applied, in order, on each conflicted file.

When one of the solver solves the last conflict in the file, remaining
solvers will be ignored.

Usually it's a good practice to leave your preferred manual solver as
the last in the tool chain. eg :

::

    [amt]
        tools = gen_simplify;gen_additions;gen_deletions;meld

Additional options
^^^^^^^^^^^^^^^^^^

You can switch on the ``verbose`` option to log, on each conflicted
file, which solvers are used on which conflict

::

    [amt]
        tools = ...
        verbose = true

The log of the process will then look like this :

::

     Normal merge conflict for 'src/main/Foo.java':
      {local}: modified file
      {remote}: modified file
     [AMT] → Trying merge with gen_simplify
     [AMT] ✗ gen_simplify didn't solve all conflicts
     [AMT] → Trying merge with gen_additions
     [AMT] ✗ gen_additions didn't solve all conflicts
     [AMT] → Trying merge with gen_deletions
     [AMT] ✗ Ignoring tool gen_deletions (unknown tool)
     [AMT] → Trying merge with gen_woven
     [AMT] ✓ gen_woven merged successfully

Keeping reports
^^^^^^^^^^^^^^^

Most automatic solvers provided within AutoMergeTool can output reports
on solved and unsolved conflicts (see `Conflict Reports <reporting>`__).
By default, AutoMergeTool deletes all report files when all conflicts
are solved. You can make AMT keep those reports even when the merge is a
success.

::

    [amt]
        tools = ...
        keepReports = true

Merge Tools
~~~~~~~~~~~

Basic configuration
^^^^^^^^^^^^^^^^^^^

The basic configuration of merge tools is the same as the standard Git
config. Here are the options every mergetool can have:

-  ``cmd`` : a specific command line invocation. The $BASE, $LOCAL,
   $REMOTE and $MERGED variables will be replace with the path of the
   corresponding files.
-  ``path`` : for `known merge tools <known_merge_tools>`__, the
   invocation uses the tool's name. If the tool is not reachable is the
   Path, you can specify a different path to the executable here. This
   is usefull when you have different versions of a tool installed on
   your computer.
-  ``trustExitCode`` : if this option is set to true, then the exit code
   of the executable will be used as an indication that the merge is
   fully successfull (or not).

Advanced configuration
^^^^^^^^^^^^^^^^^^^^^^

In addition to git's standard configuration option, AutoMergeTool can
read additional options on each tool to add advanced behavior:

-  ``extensions`` : a semi-colon separated list of file extensions to
   allow a tool to be used on specific files. Eg: if the ``extensions``
   lists ``htm;html``, the tool will only run on HTML files.
-  ``ignoreExtensions`` : a semi-colon separated list of file extensions
   to prevent a tool to be used on specific files. Eg : if
   ``ignoreExtensions`` lists ``java;kt``, the tool won't run on java
   and kotlin files.

Internal solvers
^^^^^^^^^^^^^^^^

For a detailed list of all internal solvers, and how to configure them,
see the `Known Merge Tools <known_merge_tools>`__ page.

Custom mergetools
^^^^^^^^^^^^^^^^^

AutoMergeTool has a basic configuration for a few common manual merge
tools. But if you want to use an unknown tool, or you want to configure
it yourself, you can override the default config using the options
described above.

Configuring custom merge tools uses the exact same syntax as the one
you're used to on git, and the AutoMergeTool additional parameters are
available too.

Here's an example on how you can write those :

::

    [mergetool "foo"]
        path = /usr/bin/foo.sh

    [mergetool "bar"]
        cmd = bar -o 2 --files $LOCAL $MERGED $REMOTE
        trustExitCode = true

Please note that if you provide a ``mergetool.<tool>.cmd`` value, the
``$BASE``, ``$LOCAL``, ``$REMOTE`` and ``$MERGED`` variables will be
replace with the path of the corresponding files.

Also, any unknown option (ie: one that is not listed on this page) that
you set in a ``mergetool.<tool>`` section will be added to the tool
invocation. For instance, the following config will append
``--auto-merge`` to the ``meld`` invocation command line, and
``--config ~/custom_config`` when calling ``kdiff``

::

    [mergetool "meld"]
        auto-merge =

    [mergetool "kdiff"]
        config = ~/custom_config

--------------

*For more information on configuring mergetools, see the `Official
``git-mergetool``
documentation <https://git-scm.com/docs/git-mergetool>`__*
