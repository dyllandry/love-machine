import boto3, os, random, string, botostubs
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def createMessage(client: botostubs.DynamoDB, text: string):
    """
    Creates a message in the unused messages table.
    @param db: A boto3 client.
    @param text: The message's text.
    """
    messageId = getRandomString(10)
    client.put_item(
        TableName=os.getenv('UNUSED_MESSAGES_TABLE_NAME'),
        Item={
            "messageId": { "S": messageId },
            "text": { "S": text },
            "createdAt": { "S": datetime.isoformat(datetime.utcnow()) }
        }
    )
    return messageId

def deleteMessage(client: botostubs.DynamoDB, id: string):
    """
    Deletes a message from the unused messages table.
    @param db: A boto3 client.
    @param id: The message's id.
    """
    client.delete_item(
        Key={ "messageId": { "S": id } },
        TableName=os.getenv('UNUSED_MESSAGES_TABLE_NAME')
    )

def getRandomString(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))