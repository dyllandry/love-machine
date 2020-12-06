import boto3, os, random, string, botostubs
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

_unusedTableName = os.getenv("UNUSED_MESSAGES_TABLE_NAME")
_usedTableName = os.getenv("USED_MESSAGES_TABLE_NAME")

def getMessage(client: botostubs.DynamoDB, tableName: string, id: string):
    response = client.get_item(
        Key={ "messageId": { "S": id } },
        TableName=tableName
    )
    return _getResponseToMessage(response)

def deleteMessage(client: botostubs.DynamoDB, tableName: string, id: string):
    client.delete_item(
        Key={ "messageId": { "S": id } },
        TableName=tableName
    )

def createUnusedMessage(client: botostubs.DynamoDB, text: string):
    messageId = _getUid()
    client.put_item(
        TableName=_unusedTableName,
        Item={
            "messageId": { "S": messageId },
            "text": { "S": text },
            "createdAt": { "S": datetime.isoformat(datetime.utcnow()) }
        }
    )
    return messageId

def createUsedMessage(client: botostubs.DynamoDB, createdAt: string, text: string): 
    client.put_item(
        TableName=_usedTableName,
        Item={
            "messageId": { "S": _getUid() },
            "text": { "S": text },
            "createdAt": { "S": createdAt },
            "sentAt": { "S": datetime.isoformat(datetime.utcnow()) },
        }
    )

def moveUnusedMessageToUsed(client: botostubs.DynamoDB, id: string):
    """Moves a message from the unused messages table to the used messages table."""
    message = getMessage(client=client, tableName=_unusedTableName, id=id)
    deleteMessage(client=client, tableName=_unusedTableName, id=id)
    createUsedMessage(client=client, createdAt=message["createdAt"], text=message["text"])

def _getResponseToMessage(response):
    item = response["Item"]
    message = {
        "id": item["messageId"]["S"],
        "createdAt": item["createdAt"]["S"],
        "text": item["text"]["S"]
    }
    if item.get("sentAt"): message["sentAt"] = item["sentAt"]["S"]
    return message

def _getUid():
    return _getRandomString(10)

def _getRandomString(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))