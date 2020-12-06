"""
All the database methods. Make sure the values in .env are correct.

Functions:
  -- up() Creates db stuff.
  -- down() Deletes db stuff.
"""

import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

client = boto3.client(
    'dynamodb',
    region_name=os.getenv('AWS_REGION_NAME'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    endpoint_url=os.getenv('AWS_ENDPOINT_URL')
)

def up():
    """Does first time database setup for the app, creates all the necessary db tables."""
    _createTable(os.getenv('UNUSED_MESSAGES_TABLE_NAME'))
    _createTable(os.getenv('USED_MESSAGES_TABLE_NAME'))


def _createTable(tableName):
    """Creates a table, handling the error if the table already exists."""
    try:
        client.create_table(
            TableName=tableName,
            AttributeDefinitions=[{
                'AttributeName': 'messageId',
                'AttributeType': 'S'
            }],
            KeySchema=[{
                'AttributeName': 'messageId',
                'KeyType': 'HASH'
            }],
            BillingMode='PROVISIONED',
            ProvisionedThroughput={
                'ReadCapacityUnits': 25,
                'WriteCapacityUnits': 25
            }
        )
    except ClientError as e:
        if (e.response['Error']['Code'] != 'ResourceInUseException'):
            raise e
    return


def down():
    """Tears down the database, deletes all the tables this project uses."""
    _deleteTable(os.getenv('UNUSED_MESSAGES_TABLE_NAME'))
    _deleteTable(os.getenv('USED_MESSAGES_TABLE_NAME'))


def _deleteTable(tableName):
    """Deletes a table, handling the error if the table doesn't exist."""
    try:
        client.delete_table(TableName=tableName)
    except ClientError as e:
        if(e.response['Error']['Code'] != 'ResourceNotFoundException'):
            raise e
