import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

def send(text):
    client.messages.create(
        body=text,
        from_=os.getenv("SENDER_PHONE"),
        to=os.getenv("RECIPIENT_PHONE")
    )

