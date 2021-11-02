.. _how-to-add-custom-aws-resource-searcher:

How to add custom aws resource searcher
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Understand How it works
------------------------------------------------------------------------------

**Concepts**

- Service id: an unique identifier for a main service or sub service. For example ``ec2`` is for Elastic Computer Service, ``instances`` is for EC2 instances.
- Query str: a query str that could have space, dash, underscore for searching.
- AWSResoourceSearcher class: a utility class defines the behavior of ``list resources`` and ``filter resources``, it always has a service_id associated with it. For example, ``ec2-instances`` is used to match ``Ec2InstanceSearcher`` class.

**What happens when you enter a query**

- You entered ``aws iam-roles alice`` in Alfred input box
- Your input will be parsed as ``main_service_id = iam, sub_service_id = roles, query_str = alice``
- The `AwsResourceSearcherRegistry <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res/__init__.py>`_  use the service id ``iam-roles`` as a key to locate a **custom AWS resource searcher class, this is what you need to implement**.
- In this example, the SearcherRegistry locates the `IamRolesSearcher <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res/iam_roles.py>`_ class.
- If you entered ``aws iam-roles``, the ``IamRolesSearcher.list_res`` method will be called and returns some data representing IAM role object. If you entered ``aws iam-roles alice``, the ``IamRolesSearcher.filter_res(query_str="alice")`` will be called and returns some IAM role data.
- Eventually the ``IamRolesSearcher.to_item(role)`` will be called to convert the AWS resource data (in this case it is IAM role) into ``Alfred Item`` object that defines the ``title``, ``subtitle``, ``console_url`` you see in the Alfred dropdown menu.
- You will see the rendered item in the Alfred dropdown menu, and be able to do sub-sequence actions.


Implement Custom AWS Resource Searcher
------------------------------------------------------------------------------

I use ``iam-roles`` as example to walk through the step-by-step implementation tutorial.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. Prepare the information and code skeleton
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Find the ``main_service_id`` and ``sub_service_id`` in `console-urls.yml <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/devtools/console-urls.yml>`_ file.
2. Find the AWS Python SDK boto3 api call document in `boto3 official document site <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles>`_. In this example, it is ``list_roles(**kwargs)``
3. Create a python module with naming convention ``${main_service_id}_${sub_service_id}.py`` at `aws_tools/search/aws_res <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res>`_. In this example, it is `iam_roles.py <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res/iam_roles.py>`_.
4. Copy codes from ``aws_res/ec2_instances.py`` as a starting point.


2. Implement your custom search logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Define a simple data container class to simplify your code. In this example, it is ``class Role``.
    - visually check the attributes you need from the `boto3 response syntax <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles>`_, and declare the attribute like the syntax at `class Role(ResData): <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res/iam_roles.py>`_
    - custom the ``def to_console_url(self):`` method, it should return the AWS console url locate the resource. For regional resource it needs a ``{region}`` placeholder in the f-string template. Example: ``https://console.aws.amazon.com/ec2/v2/home?region={region}#InstanceDetails:instanceId={inst_id}``
    - custom the ``def to_large_text(self):`` method, it returns large text to show when you hit ``cmd + L``.
    - custom the ``def id(self):`` property method, id should be the unique identifier of this data object. It allows you to deduplicate the object based on the id.
2. Define a ``AWSResourceSearcher`` subclass to implement the ``list_res`` and ``filter_res`` logic. In this example, it is `class IamRolesSearcher <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res/iam_roles.py>`_.
    - define the ``id`` attribute, it is ``${main_service_id}.${sub_service_id}``. So the Searcher register can find it.
    - define the ``simplify_response`` method, it converts the `boto3 response syntax <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles>`_ into list of the data object. In this example, it is ``class Role``
    - define the ``list_res`` method, it calls the boto3 api and returns list of data object to display in the Alfred dropdown menu. You can use ``@cache.memoize(expire=SettingValues.expire)`` decorator to cache the output.
    - define the ``filter_res`` method, it calls the boto3 api and returns list of filtered data object to display in Alfred dropdown menu. You can also use the same decorator to cache the output.
    - define the ``to_item`` method, it converts the data object to an Alfred ``ItemArgs`` object representing an Alfred dropdown menu item.
3. Enable the Searcher:
    - import this Searcher class in the `register module <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/aws_tools/search/aws_res/__init__.py>`_ and register it.


3. Test your Searcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow `this pattern <https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/tests/search_aws_res/test_iam_roles.py>`_ and test the searcher with custom ``query_str``.


References
------------------------------------------------------------------------------

- Emoji: https://emojipedia.org/
    - Symbol: https://emojipedia.org/symbols/
