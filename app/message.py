import boto3, os, random, string
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

_unusedTableName = os.getenv("UNUSED_MESSAGES_TABLE_NAME")
_usedTableName = os.getenv("USED_MESSAGES_TABLE_NAME")

def getRandomUnusedMessage(client):
    response = client.scan(TableName=_unusedTableName, Limit=10)
    messages = map(lambda item: _itemToMessage(item), response["Items"])
    return random.choice(list(messages))

def createUsedMessage(client, createdAt: string, text: string): 
    client.put_item(
        TableName=_usedTableName,
        Item={
            "messageId": { "S": _getUid() },
            "text": { "S": text },
            "createdAt": { "S": createdAt },
            "sentAt": { "S": datetime.isoformat(datetime.utcnow()) },
        }
    )

def deleteUnusedMessage(client, id: string):
    client.delete_item(
        Key={ "messageId": { "S": id } },
        TableName=_unusedTableName
    )

def createUnusedMessage(client, text: string):
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

def formatAsSms(text, createdAt):
    return os.getenv("RECIPIENT_NAME") + ",\n" + text + "\n\n -- Written with love at " + datetime.fromisoformat(createdAt).strftime("%A %H:%M, %B %d, %Y")

def _itemToMessage(item):
    """Converts a DynamoDB response item to a message dict."""
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
