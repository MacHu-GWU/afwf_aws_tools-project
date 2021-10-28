AWS Console Launcher Tutorial
==============================================================================

AWS Console Launcher allows you to quickly open AWS Console pointing to:

- Specific AWS Service, for example: ec2, s3, ...
- Specific Sub AWS Servicie, for example: ec2-instances, ec2-securitygroups, ec2-ebsvolumes, ...
- Specific AWS Resource filter, for example: ec2-instances i-abcd1234, ....

``aws`` is the keyword to trigger the AWS Console Launcher workflow. You can change it to anything in Alfred Workflow preference.

The full syntax is: ``"aws ${service_identifier} ${query}"``.



Alfred Input Box Behavior
------------------------------------------------------------------------------

Term:

- main service: top level aws service, for example: ec2, s3, ...
- sub service: secondary level aws service that related to specific main service, for example: ec2-instances, ec2-securitygroups, ...

``"aws"``:

- behavior: list all alfred keyword related to ``"aws"``
- tab: auto complete to ``"aws "``
- enter: same as tab

``"aws "``:

- behavior: list all main services, for example, ec2, s3, ...
- tab: do nothing
- enter: do nothing

``"aws {query}"``:

- example: ``"aws e"``
- behavior: filter main services based on the query, for example, ec2, ecr, ecs, ...
- tab: auto complete to ``"aws ec2-"``
- enter: open the aws service console in browser for the selected main service, for example, ``https://console.aws.amazon.com/ec2/v2/home``

``"aws ec2-"``:

- behavior: list all related sub services, for example, ec2-instances, ec2-securitygroups, ec2-ebsvolumes, ... first item is always the main service ifself, for example ``https://console.aws.amazon.com/ec2/v2/home``
- tab: do nothing
- enter: open the selected main or sub service console in browser for the selected sub service, for example, ``https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances: ``

``"aws ec2-{query}"``:

- example: ``"aws ec2-ins"``
- behavior: filter sub services based on the query, for example, ec2-instances.
- tab: auto complete to ``"aws ec2-instances "``
- enter: open the aws service console in browser for the selected sub service, for example, ``https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances: ``

``"aws ec2-instances "``

- behavior: list all related resources, for example, list of security group name and ids. first item is always the sub service itself, for example, ``https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances: ``
- tab: do nothing
- enter: open the selected sub service console in browser for the selected sub service, for example, ``https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances: ``

``"aws ec2-instances {query}"``

- example: ``"aws ec2-instances dev"``
- behavior: filter resources based on the query, for example, ec2-instances tag:name=infra-dev
- tab:
- enter:

- behavior:
- tab:
- enter:

- behavior:
- tab:
- enter: