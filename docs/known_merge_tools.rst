Known Merge Tools
-----------------

Internal tools refer to automatic conflict solvers bundled with AMT.

External tools refer to 3rd party, usually manual, merge tools. They are
known in the sense that you don't have to configure their command line
invocation.

Internal (Language agnostic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simplify Conflicts (``gen_simplify``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool will handle any conflict for which a large block of code is
reported as a single conflict, by splitting it in smaller conflict which
can be then each be solved by other tools. It's reccomended to use this
as the first tool in the ``amt.tools`` option.

You can add the following options :

-  **mergetool.gen\_simplify.report** : sets the type of report (cf
   `Conflict Reports <reporting>`__)
-  **mergetool.gen\_simplify.verbose** : when set to true, logs this
   solver's process in the console output.

Woven Conflicts (``gen_woven``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tool will handle any conflict for which the local and remote modify
different lines (eg: local modifies lines 1,2 and 5, remote modifies
lines 3 and 4).

You can add the following options :

-  **mergetool.gen\_woven.report** : sets the type of report (cf
   `Conflict Reports <reporting>`__)
-  **mergetool.gen\_woven.verbose** : when set to true, logs this
   solver's process in the console output.

Addition Conflicts (``gen_additions``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool will handle any conflict for which the local and remote
versions add content in the same place.

You can add the following options :

-  **mergetool.gen\_additions.order** : sets the preference when adding
   both sides; can be ``remotefirst`` (default), ``localfirst``, or
   ``ask``
-  **mergetool.gen\_additions.report** : sets the type of report (cf
   `Reporting <Reporting>`__)
-  **mergetool.gen\_additions.verbose** : when set to true, logs this
   solver's process in the console output.
-  **mergetool.gen\_additions.whitespace** : when set to true, treats
   replacement of whitespace and new lines as additions.

Deletions Conflicts (``gen_deletions``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool will handle any conflict for which the local and remote
versions both deleted the same content.

You can add the following options :

-  **mergetool.gen\_deletions.report** : sets the type of report (cf
   `Conflict Reports <reporting>`__)
-  **mergetool.gen\_deletions.verbose** : when set to true, logs this
   solver's process in the console output.

Internal (Language specific)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JavaImports (``java_imports``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool will handle any conflict within the imports section of your
java files.

You can add the following options :

-  **mergetool.java\_imports.order** : specify the way to order imports.
   Presets include Android Studio : ``android``; IntelliJ Idea :
   ``idea``; and Eclipse : ``eclipse``
