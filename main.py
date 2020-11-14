# Connects with a local DynamoDB server.

import boto3

client = boto3.client(
  "dynamodb",
  region_name="none",
  aws_access_key_id="none",
  aws_secret_access_key="none",
  endpoint_url="http://localhost:8000"
)

response = client.list_tables()

print(response)