import requests
import json
from pprint import pprint
import os


user = os.environ.get("SP_USER_KEY")


def handler(event, context):
    url = "https://api.statuspage.io/v1/"

    headers = {
        "Authorization": "OAuth " + user,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {}

    pages = requests.get(url + "pages",
                 headers=headers,
                 params=params)
    pages = pages.json()
    pageId = next((p['id'] for p in pages if event['Page'].lower() == p['name'].lower()), False)

    components = requests.get(url + "pages/" + pageId + "/components",
                         headers=headers,
                         params=params)
    components = components.json()

    compId = next((c['id'] for c in components if event['Component'].lower() == c['name'].lower()), False)

    if True:
        payload = json.dumps({
            "component": {
                "status": event['Status']
            }
        })

        update = requests.put(url + "pages/" + pageId + "/components/" + compId,
                                  headers=headers,
                                  params=params,
                                  data=payload)
        print(update.status_code)
        results = update.json()
        print(results)
        return "Status Has Been Updated."

#event = {"Page": "RigD", "Component": "RigD App", "Status": "major_outage"}

#print(handler(event,""))