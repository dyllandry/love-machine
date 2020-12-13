import os
from dotenv import load_dotenv
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

load_dotenv()

configuration = clicksend_client.Configuration()
configuration.username = os.getenv("CLICKSEND_USERNAME")
configuration.password = os.getenv("CLICKSEND_PASSWORD")

clicksendApi = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

def send(text):
    smsMessage = SmsMessage(
        to=os.getenv("RECIPIENT_PHONE"),
        _from=os.getenv("SENDER_PHONE"),
        body=text,
    )
    smsMessages = clicksend_client.SmsMessageCollection(messages=[smsMessage])
    try:
        clicksendApi.sms_send_post(smsMessages)
    except ApiException as e:
        print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
    return