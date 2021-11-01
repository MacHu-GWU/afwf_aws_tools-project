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

**Navigate to AWS service and it's sub service**

Usage:

- Type``aws ${main_service}`` or ``aws ${main_service}-${sub_service}``.
- hit "Tab" to auto complete the search string.
- hit "Enter" to open the AWS Console.

Note:

    It support full text search. For example, ``st`` can match ``instances``, ``sg`` can match ``Security Group``.

.. image:: https://user-images.githubusercontent.com/6800411/139746691-752009fd-7a57-4429-a315-37d496e26a33.gif

.. image:: https://user-images.githubusercontent.com/6800411/139746689-ef72be04-d4d2-487f-a748-7b0c0056ee1d.gif







Navigate AWS Console Fast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you have many named profile defined in ``~/.aws/credentials`` and ``~/.aws/config``. **Now you can easily set one of the named profile as DEFAULT profile**! Basically this workflow will update the ``~/.aws/credentials`` and ``~/.aws/config`` accordingly.

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
