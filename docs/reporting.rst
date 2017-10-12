Conflict Reports
----------------

Most internal tools bundled in AMT have a report feature, that writes a
report file next to conflicted files.

Configuration
~~~~~~~~~~~~~

To enable reporting, you only need to add the following lines in your
global ``~/.gitconfig`` file, or in your project's ``.git/config`` file.

::

    [mergetool "xyz"]
        report = none|solved|unsolved|full

The possible values are : - **none** : no report will be written -
**solved** : the report file will only log conflicts solved by the
``xyz`` tool - **unsolved** : the report file will only log conflicts
that the ``xyz`` tool could not solve - **full** : the report file will
report both solved and unsolved files

Reporting output
~~~~~~~~~~~~~~~~

The report file for a file ``path/to/foo.ext`` will be
``path/to/foo.ext.xyz-report``.

*Note: AMT automatically deletes report files when a when a conflict is
successfully solved. If you want to keep the reports anyway, you can add
the following configuration :*

::

    [amt]
        keepReport = true
