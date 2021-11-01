.. _release_history:

Release and Version History
==============================================================================


1.0.2 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
