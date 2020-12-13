import db, message, sms

def sendMessage():
    unusedMessage = message.getRandomUnusedMessage(db.client)
    smsMessageText = message.formatAsSms(text=unusedMessage["text"], createdAt=unusedMessage["createdAt"])
    sms.send(smsMessageText)
    message.createUsedMessage(db.client, createdAt=unusedMessage["createdAt"], text=unusedMessage["text"])
    message.deleteUnusedMessage(db.client, unusedMessage["id"])
    return
