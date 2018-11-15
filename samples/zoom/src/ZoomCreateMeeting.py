"""This is an example AWS Lambda module that provides
fulfillment for a RigD user-defined activity."""
import os
import json
from time import time, gmtime, strftime
import pprint as pp
import urllib.parse
import requests
import jwt

API_KEY = os.environ.get("ZOOM_API_KEY")
API_SECRET = os.environ.get("ZOOM_API_SECRET")
API_USER_ID = os.environ.get("ZOOM_UID")  # e-mail address of a Zoom user

INSTANT_MEETING = 1
SCHEDULED_MEETING = 2


def get_jwt_token(ttl_sec=60):
    """JWT token from API KEY.  Zoom API v2 uses JWT for security"""
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": API_KEY,
        "exp": int(time() + ttl_sec)
    }
    return jwt.encode(payload, API_SECRET, algorithm='HS256', headers=header).decode()


MSG_SUCCESS = [
    {"mrkdwn_in": ["text",
                   "fields",
                   "pretext"],
     "pretext": "*Click on the button below to join*",
     "color": "good",
     "fallback": "",
     "actions": [{
         "type": "button",
         "text": "👉Join now",
         "url": ""
     }],
     "fields": [
         {
             "title": "Zoom Meeting Started",
             "value": "Click below to join:",
             "short": False
         }
     ]
    }
]


def slack_msg_success(url, mid):
    """fill the slack message template with url and meeting ID"""
    msg = MSG_SUCCESS
    msg[0]['actions'][0]['url'] = url
    msg[0]['fallback'] = "Join meeting: %s" % url
    msg[0]['fields'][0]['value'] = 'Meeting ID: %d' % mid
    return msg


MSG_FAILURE = [
    {
        "mrkdwn_in": ["text", "fields", "pretext"],
        "pretext": "*Failed to start Zoom meeting*",
        "color": "danger",
        "text": "empty",
        "fields": [{"title": "Error",
                    "value": "Please, try again!",
                    "short": False
                   }]
    }
]


def slack_msg_failure(error_msg):
    """fill the slack failure message template with an error message"""
    msg = MSG_FAILURE
    msg[0]['text'] = error_msg
    return msg


def handler(event, context):
    """The main entry point of the lambda module.
    Gets called when your custom activity needs fulfillment"""

    def set_value(field_name, default):
        """extract a parameter value from the event if set, return the default otherwise"""
        if field_name in event:
            val = event[field_name]
            if val == 'y':
                return True
            elif val == 'n':
                return False
            return val
        return default

    if API_KEY is None or API_SECRET is None or API_USER_ID is None:
        slack_msg = slack_msg_failure("One or more credentials are missing.  Please, ensure "
                                      "that ZOOM_API_KEY, ZOOM_UID, and "
                                      "ZOOM_API_SECRET are set properly.")
    else:
        settings = {
            'join_before_host': set_value('join_before_host', False),
            'host_video': set_value('host_video', False),
            'participant_video': set_value('participant_video', False),
            'mute_upon_entry': set_value('mute_upon_entry', False),
            'watermark': set_value('watermark', False),
            'approval_type': set_value('approval_type', 2),
            'registration_type': set_value('registration_type', 1),
            'use_pmi': set_value('use_pmi', None),
            'audio': set_value('audio', 'both'),
            'auto_recording': set_value('auto_recording', 'none'),
            'enforce_login': set_value('enforce_login', False),
            'enforce_login_domains': set_value('enforce_login_domains', ""),
            'alternative_hosts': set_value('alternative_hosts', "")
        }
        req = {
            "topic": event['topic'] if 'topic' in event else 'RigD-created meeting',
            "type": SCHEDULED_MEETING,
            "start_time": strftime("%Y-%m-%d'T'%H:%M:%S'Z'", gmtime()),  # start now
            "timezone": 'UTC',
            "duration": set_value('duration', 60),  # minutes
            "password": event['password'] if 'password' in event else None,
            "agenda": event['agenda'] if 'agenda' in event else 'Item 1: Playing ' \
                                                                'with RigD Custom Activities',
            "settings": settings
        }
        base_url = "https://api.zoom.us/v2/users/%s/meetings" % urllib.parse.quote(API_USER_ID)
        try:
            res = requests.post(url=base_url, data=json.dumps(req),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': 'Bearer %s' % get_jwt_token(20)})
            response = json.loads(res.text)

            if res.status_code != 201:
                slack_msg = slack_msg_failure("%d %s %s" % (res.status_code,
                                                            res.reason, response['message']))
            else:
                url = response['join_url']
                slack_msg = slack_msg_success(url, response['id'])

        except Exception as ex:
            slack_msg = slack_msg_failure("An exception occurred %s" % ex)

    resdict = {"format": "Slack", "message": slack_msg}
    return resdict


def main():
    """For local testing. Will be ignored by AWS"""
    tevt = {
        "join_before_host": True
    }
    pp.pprint(handler(tevt))


if __name__ == "__main__":
    main()
