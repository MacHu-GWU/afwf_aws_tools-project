Alfred Workflow - AWS Tools
==============================================================================

.. contents::
    :depth: 1
    :local:


Features
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


💥 Navigate AWS Console Fast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Navigate to AWS service and it's sub service**

Usage:

- Type ``aws ${main_service}`` or ``aws ${main_service}-${sub_service}``.
- hit "Tab" to auto complete the search string.
- hit "Enter" to open the AWS Console.

Note:

- It support full text fuzzy search. For example, ``st`` can match ``instances``, ``sg`` can match ``Security Group``.
- If an AWS service has sub services, there's is a 📂 icon.

.. image:: https://user-images.githubusercontent.com/6800411/139746691-752009fd-7a57-4429-a315-37d496e26a33.gif

.. image:: https://user-images.githubusercontent.com/6800411/139746689-ef72be04-d4d2-487f-a748-7b0c0056ee1d.gif

**2. Search AWS Resource and see it in Console**

Usage:

- Type ``aws ${main_service}-{sub_service}`` or find the sub service then hit "Tab" to search AWS resources (if available).
- Type any search string to filter the resource. Example: ``aws iam-roles dev``

Note:

- It support full text fuzzy search on ``Name`` and ``id`` (if available). For example: ``7d4f`` can match an EC2 instance ``i-abcd...7d4f``.
- If an AWS sub services support resources search, there's is a 🔍 icon.

.. image:: https://user-images.githubusercontent.com/6800411/139746690-ae2fcf1e-cd84-4d02-ad02-0103248b9b5b.gif

**3. Copy ARN to Clipboard**

Usage:

- Type ``aws  ${main_service}-{sub_service} ${query}`` to locate the resource. And Press down "Alt" then hit "Enter" to copy ARN to clipboard (if available).

.. image:: https://user-images.githubusercontent.com/6800411/139749561-93b1b8e6-c5ee-4890-a82a-d4bcf922da16.gif


Switch Default AWS Profile for CLI / SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you have many named profile defined in ``~/.aws/credentials`` and ``~/.aws/config``. **Now you can easily set one of the named profile as DEFAULT profile**. Basically this workflow will update the ``~/.aws/credentials`` and ``~/.aws/config`` accordingly.

For example, ``~/.aws/config``::

    # content of ~/.aws/config
    [default]
    region =
    output =

    [profile aws_dev]
    region = us-east-1
    output = json

    [profile aws_stage]
    region = us-east-2
    output = json

    [profile aws_prod]
    region = us-west-1
    output = json


and ``~/.aws/credentials``::

    # content of ~/.aws/credentials
    [default]
    region =
    output =

    [aws_dev]
    aws_access_key_id = AAA
    aws_secret_access_key = AAA

    [aws_stage]
    aws_access_key_id = BBB
    aws_secret_access_key = BBB

    [aws_prod]
    aws_access_key_id = CCC
    aws_secret_access_key = CCC

Type ``aws-cli-set-profile dev`` to filter the named profile, hit "Enter" to set it as default.

.. image:: https://user-images.githubusercontent.com/6800411/139747808-aaca4158-c86c-4d9e-afc9-63acf30e40b3.gif

It will pop a notification to tell you which profile is set.

.. image:: https://user-images.githubusercontent.com/6800411/139746693-f671ad07-51cc-4d24-9c4a-500fccb64827.png

Then the ``~/.aws/config`` becomes::

    [default]
    region = us-east-1
    output = json

The ``~/.aws/credentials`` becomes::

    [default]
    aws_access_key_id = AAA
    aws_secret_access_key = AAA


.. image:: https://user-images.githubusercontent.com/6800411/128253078-c6d1c06e-6e17-48e9-86d1-6be67cbfa27a.gif


MFA Auth Based on One of the AWS Named Profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For security concern, **some organization requires MFA auth before using AWS API Key**. In other words, you need to run ``aws sts get-session-token --serial-number arn-of-the-mfa-device --token-code code-from-token`` commands and manually update your ``~/.aws/credentials`` file and use your new temporary named profile. (Official document can be found here https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/)

This workflow allows you to type::

    aws-mfa-auth ${your_base_named_profile} ${six_digits_mfa_token_from_your_phone}

Then a new aws profile ``${your_base_named_profile}_mfa`` (with ``_mfa`` surfix) will be instantly ready to use.


Install
------------------------------------------------------------------------------

**Installation**:

Go to https://github.com/MacHu-GWU/afwf_aws_tools-project/releases, download the latest ``AWS Tools.alfredworkflow`` file, double click to install.
