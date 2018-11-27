import requests
from requests.auth import HTTPBasicAuth
import json
import os


user = os.environ.get("JIRA_USER")
token = os.environ.get("JIRA_TOKEN")


auth = HTTPBasicAuth(user, token)

def handler(event, context):
    url = "https://rigdio.atlassian.net/rest/servicedeskapi/"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-ExperimentalApi": "opt-in"
    }

    params = {}

    # find the service desk
    sDesks = requests.get(url + "servicedesk",
                        headers=headers,
                        auth=auth,
                        params=params)

    sDesks = sDesks.json()

    deskId = next((d['id'] for d in sDesks['values'] if event['ServiceDesk'] in [d['projectName'], d['projectKey']]), False)
    if not deskId:
        failure = "Could not find that service desk."
        return failure

    # find the request type
    rTypes = requests.get(url + "servicedesk/" + deskId + "/requesttype",
                        headers=headers,
                        auth=auth,
                        params=params)
    rTypes = rTypes.json()

    rTypeId = next((r['id'] for r in rTypes['values'] if event['RequestType'] == r['name']), False)
    if not rTypeId:
        failure = "Could not find that request type. It must have one of the these values. \n (" + str([r['name'] for r in rTypes['values']]) + ")"
        return failure

    rFields = requests.get(url + "servicedesk/" + deskId + "/requesttype/" + rTypeId + "/field",
                        headers=headers,
                        auth=auth,
                        params=params
                        )
    rFields = rFields.json()

    rfields = rFields['requestTypeFields']
    fmap={
    }
    for f in rfields:

        found = next((v for k, v in event.items() if k in [f['fieldId'], f['name']]), False)
        if not found and f['required']:
            failure = "Sorry, The field, " + f['name'] + ", is required. "
            return failure
        elif len(f['validValues']) > 0 and found not in f['validValues']:
            failure = "Sorry, The field, " + f['name'] + ", must have one of the these values. \n (" + str(f['validValues']) + ")"
            return failure
        elif not found:
            continue

        fmap.update({f['fieldId']:found})


    if True:
        payload = json.dumps({
            "serviceDeskId": deskId,
            "requestTypeId": rTypeId,
          "requestFieldValues": fmap
        })


        ticket = requests.post(url + "request",
                            headers=headers,
                            auth=auth,
                            data=payload
                            )
        if '20' in str(ticket.status_code):
            results = ticket.json()
            link = results['_links']['web']
            response = {"Created Ticket": results['issueKey'], "Jira Ticket Link": link}
            return response
        else:
            print(ticket.json())
            return "Failed to Create Ticket"


#event={'RequestType': 'IT help', 'ServiceDesk': 'SWAB1', 'summary': 'There is a Problem!', 'description': 'The ship has a hole in it.', 'PagerDuty Url': 'https://rigd-io.pagerduty.com/incidents/PF0WYS8'}
#print(handler(event, ""))