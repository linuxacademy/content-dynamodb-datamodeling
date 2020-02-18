#!/bin/sh

FUNCTION_NAME=MusicTagger
ROLE_NAME=$FUNCTION_NAME-Role

# Delete Lambda function

fn_arn=$(aws lambda get-function --function-name $FUNCTION_NAME \
  --output text --query 'Configuration.FunctionArn')

if [[ $? -eq 0 ]]; then
  echo "$FUNCTION_NAME exists. Deleting ARN=$fn_arn"
  aws lambda delete-function \
    --function-name $FUNCTION_NAME
fi

# Detach policies from role
aws iam detach-role-policy --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam detach-role-policy --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Delete IAM exection role

arn=$(aws iam get-role --role-name $ROLE_NAME --output text --query 'Role.Arn')

if [[ $? -eq 0 ]]; then
  echo "$ROLE_NAME exists. ARN=$arn"
  aws iam delete-role --role-name $ROLE_NAME
fi