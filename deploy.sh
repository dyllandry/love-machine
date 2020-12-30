#!/bin/bash

awsFuncNotFound=254

source ./.env

# Setup env vars
export AWS_DEFAULT_REGION=$AWS_REGION_NAME
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# Check if exists
echo "Checking if function exists..."
aws lambda get-function \
  --function-name $LAMBDA_FUNCTION_NAME &> /dev/null

if [ $? -eq 0 ]; then
  echo "Function exists."
  echo "Deleting function..."
  aws lambda delete-function --function-name $LAMBDA_FUNCTION_NAME
  echo "Deleted."
else
  echo "Function does not exist.\n"
fi

echo "Creating function..."
aws lambda create-function \
  --function-name $LAMBDA_FUNCTION_NAME \
  --role $LAMBDA_FUNCTION_ROLE \
  --zip-file fileb://dist/deployment-package.zip \
  --runtime python3.8 \
  --handler lambdaHandler.sendMessage \
  --timeout 10 \
  --environment "Variables={ \
      UNUSED_MESSAGES_TABLE_NAME=$UNUSED_MESSAGES_TABLE_NAME, \
      USED_MESSAGES_TABLE_NAME=$USED_MESSAGES_TABLE_NAME, \
      TWILIO_ACCOUNT_SID=$TWILIO_ACCOUNT_SID, \
      TWILIO_AUTH_TOKEN=$TWILIO_AUTH_TOKEN, \
      RECIPIENT_PHONE=$RECIPIENT_PHONE, \
      RECIPIENT_NAME=$RECIPIENT_NAME, \
      SENDER_PHONE=$SENDER_PHONE, \
    }" > /dev/null
echo "Function created."
