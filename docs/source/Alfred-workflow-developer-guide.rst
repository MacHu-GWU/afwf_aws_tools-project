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


对于 Alfred UI 交互逻辑的抽象
------------------------------------------------------------------------------

首先我们来回顾一下 Alfred UI 交互的场景 ``{trigger_keyword} {query}``.

1. 在 Alfred Input Box 中, 每当我们输入一些 query, dropdown menu 就会出现一些选项, 选定一个选项按下 Tab 就是 auto complete, Enter 就是 arg.
2. 在输入 query 的过程中, 一个非常常见的应用就是在输入 query 前后台就会有许多 choice 可供选择. 这些 choice 可以在 dropdown menu 中展示也可以不展示. 而在输入 query 之后我们对 choice 进行 filter 并排序, 有时还会加一些 helper 的 row.

这时我们可以将这个场景抽象为两个概念:

1. item filter: 一个根据 query 返回一些数据的函数, query 为 null 则返回特定的数据, 不为 null 则执行一定的 filter 逻辑.
2. item builder: 一个根据数据创建 dropdown menu item 的函数. item builder 本质上是一个 handler function 也是要接受 workflow 为第一个参数.

这两者之间的排列组合可以实现非常多的功能, 从而实现代码复用.
