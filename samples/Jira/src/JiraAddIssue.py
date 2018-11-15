import requests
import json
from pprint import pprint
import os


user = os.environ.get("JIRA_USER")
token = os.environ.get("JIRA_TOKEN")

def handler(event, context):
    url = "https://rigdio.atlassian.net/rest/api/3/issue"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {"projectKeys": event['project'], "issuetypeNames": event['issuetype']}

    #meta = requests.get(url + "/createmeta",
    #                    headers=headers,
    #                    auth=(user, token),
    #                    params=params
    #                    )

    #print(pprint(meta.json()))

    payload = json.dumps( {

      "fields": {
        "project": {
          "key": event['project']
        },
        "issuetype": {
          "name": event['issuetype']
        },
          "summary":  event['summary']
      }
    })


    issue = requests.post(url,
                        headers=headers,
                        auth=(user, token),
                        data=payload
                        )
    if '20' in str(issue.status_code):
        results = issue.json()
        link = results['self'][:results['self'].find('.net/')+4] + "/projects/" + event['project'] + "/issues/" + results['key']

        pprint(url)
        response = {"Created Issue": results['key'], "Jira Link": link}
        return response
    else:
        return "Failed to Create Issue"



