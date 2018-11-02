"""This is an example AWS Lambda module that provides
fulfillment for a RigD user-defined activity."""
import os
# Download the helper library from https://www.twilio.com/docs/python/install
import twilio.base
from twilio.rest import Client


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")


def lambda_handler(event, context):
    """The main entry point of the lambda module.
    Gets called when your custom activity needs fulfillment"""

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    slack_msg = [
        {
            "mrkdwn_in": ["text", "fields", "pretext"],
            "pretext": "*Twilio API call results*",
            "color": "good",
            "text": "empty",
            "fields": [{"title": "Twilio API call",
                        "value": "",
                        "short": False
                       }]
        }
    ]

    try:
        message = client.messages \
            .create(
                body=event['Body'],
                from_=TWILIO_PHONE_NUMBER,
                to=event['To']
            )
        slack_msg[0]['text'] = "Yor message has been " + message.status
    except twilio.base.exceptions.TwilioRestException as ex:
        slack_msg[0]['text'] = ex.msg.replace("\"", "\'")
        slack_msg[0]['color'] = "danger"
    resdict = {"format": "Slack", "message": slack_msg}
    return resdict


def main():
    """For local testing. Will be ignored by AWS"""
    tevt = {
        "To": "+15005550006",
        "Body": "Hi, λ test",
    }
    import pprint as pp
    pp.pprint(lambda_handler(tevt))


if __name__ == "__main__":
    main()
