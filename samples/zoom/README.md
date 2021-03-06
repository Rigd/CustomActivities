##### Purpose
This is an AWS lambda module that allows custom activities to configure and start Zoom meetings.
##### Deployment
- Clone the repository
- Zip this directory (zoom) with the provided utility:  
    `sh utils/packlambda.sh zoom`
- Use RigD's "create lambda function" activity to deploy the lambda to AWS 
    - use "Python 3.6" runtime
- Set the following environment variables in the newly created lambda:
    - *ZOOM_API_KEY* - available [from Zoom](https://support.zoom.us/hc/en-us/community/posts/115010739366-How-to-find-API-Key-API-Secret-)
    - *ZOOM_API_SECRET* - available [from Zoom](https://support.zoom.us/hc/en-us/community/posts/115010739366-How-to-find-API-Key-API-Secret-)
    - *ZOOM_UID* - the e-mail ID of the Zoom account that will host the meeting
- Use RigD's "create rigd custom activity" command to define your meeting-starting activity (all slots are optional)
- Use one of the sample utterances you provided in the activity definition to start a Zoom meeting