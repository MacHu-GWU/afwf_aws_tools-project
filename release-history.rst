.. _release_history:

Release and Version History
==============================================================================


1.0.8 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.7 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``aws-set-profile-for-everything`` workflow, you can choose a named aws profile from your ``~/.aws/config`` for AWS Tool workflow to use and also update the ``~/.aws/config`` and ``~/.aws/credential`` file

**Minor Improvements**

- add AWS Augmented ai sub service navigator
- add AWS IAM create role / create policy navigator


1.0.6 (2022-02-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add AWS US gov cloud support
- add searcher: system manager parameter store

**Minor Improvements**

**Bugfixes**

- show found nothing message when resource search receives no query.

**Miscellaneous**


1.0.5 (2021-12-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add searcher: cloud9 environment, ide
- add ICON for 20+ top level services

**Minor Improvements**

- update elasticsearch service to opensearch, add sub services for opensearch
- add sub services for sagemaker

**Bugfixes**

**Miscellaneous**


1.0.4 (2021-11-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

- add searcher: kms, secretsmanager

**Bugfixes**

- fix bug that glue tables cannot return results

**Miscellaneous**


1.0.3 (2021-11-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- auto build console url index.
- add logger that log info and error track back to ``~/.alfred-aws-tools``.
- add ``aws-tool-clear-log`` trigger.
- add ``aws-tool-set`` trigger, it can set the global setting key/value pair.

**Minor Improvements**

- add searcher: glue, lambda, lakeformation, cloudformation, dynamodb
- allow in-console search, for example: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:search=dev
- improve query performance, latency is reduced from 0.3 sec to 0.01 sec by setting index.

**Bugfixes**

**Miscellaneous**


1.0.2 (2021-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Allow multi token full text search. For example: ``aws ec2-instances alice dev``. Before it only supports ``aws ec2-instances alice``

**Minor Improvements**

- Show helper information when AWS Service id / Sub service id is wrong.
- Add `How to add custom aws resource searcher <./docs/source/How-to-add-custom-aws-resource-searcher.rst>`_ document.

**Bugfixes**

**Miscellaneous**

- Refact the AWSResourceSearch class to make writing custom AWS resource search easier.


1.0.1 (2021-11-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``aws-tool-set-profile`` workflow, you can choose a named aws profile from your ~/.aws/config for AWS Tool workflow to use.
- add ``aws-tool-set-region`` workflow, you can choose a aws region for AWS Tool workflow to use.
- add ``aws-tool-clear-cache`` workflow to clear aws-tool cache.
- add ``aws-tool-rebuild-index`` workflow to rebuild the full text search index for AWS console url searching.
- 💥 add ``aws`` workflow, **the most powerful aws console url navigator**
    1. navigate to AWS Service (like EC2) or sub service (like IAM.Role)
    2. filter AWS resources like EC2 instance, Security Group, IAM role and see it in AWS console
    3. copy ARN (AWS Resource Name) to clipboard

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.3 (2021-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``aws-mfa-auth`` workflow, allow quick set a new mfa auth named profile using a base named profile and your six digits mfa token.


0.0.2 (2021-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- The default profile name in ``~/.aws/config`` should be ``[default]``. In 0.0.1, it was ``[profile default]``


0.0.1 (2021-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Birth!
- add ``aws-set-default-profile`` workflow, allow set one of aws named profile from ``~/.aws/credentials`` as DEFAULT
