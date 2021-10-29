In this workflow, I implements the UI logic primary with `Script Filter <https://www.alfredapp.com/help/workflows/inputs/script-filter/>`_. The Script caller syntax is always ``/usr/bin/python main.py '{handler_identifier} {query}'``. I choose to use this syntax and manage the arg-parse, python function call with in application code because it's easier to manage and debug. The ``handler_identifier`` is unique key for a ``handler function`` so the python code can locate which ``handler function`` to call. The ``handler function`` is simply a normal python function that has two arguments ``wf`` representing the ``workflow.workflow3.Workflow3`` object and ``query_str`` representing additional arguments.

In handler module, there are four major type of functions:

1. main handler: takes two arguments ``wf`` and ``query_str``.  will be invoked from alfred workflow GUI editor using ``/usr/bin/python main.py '{handler_identifier} {query}'``.
2. sub handler: may take more than two arguments but the first argument is still always ``wf``. will be called from other main handler. The function name will NOT be indexed as a handler identifier, and will not be directly invoked from alfred workflow GUI.
3. item builder: a function takes ``wf`` and additional arguments, run ``Workflow3.add_item`` accordingly.
4. handler helpers: just utility functions.

Naming convention:

1. main handler: starts with ``mh_``
2. sub handler: starts with ``sh_``
3. item builder: starts with ``ib_``
4. handler helpers: any, just regular function
