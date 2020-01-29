# Amazon DynamoDB Data Modeling

Before running the code in this repo, please follow these steps to setup your workspace if you have not
set it up already:

Setup credentials for DynamoDB access. One of the ways to setup credentials is to add them to `~/.aws/credentials` file (`C:\Users\USER_NAME\.aws\credentials` file for Windows users) in following format:

```text
[<profile_name>]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

If `<profile_name>` is specified as "default" then AWS SDKs and CLI will be able to read the credentials without any additional configuration. But if a different profile name is used then it needs to be specified while initializing DynamoDB client via AWS SDKs or while configuring AWS CLI.

Please refer following guide for more details on credential configuration: <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration>

Install the latest Boto 3 release via pip:

```sh
pip install boto3
```

Please refer following guide for more details on Boto 3 installation: <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation>

Please note that you may need to follow additional setup steps for using Boto 3 from an IDE. Refer your IDE's documentation if you run into issues.
