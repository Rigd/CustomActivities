 
 
 ####Deployment
- Copy the source to your Codecommit repository
- Use RigD's "create lambda function" activity to deploy to AWS
- Set the following environment variables in the newly created lambda:
    - *ZOOM_API_KEY* - available [from Zoom](https://support.zoom.us/hc/en-us/community/posts/115010739366-How-to-find-API-Key-API-Secret-)
    - *ZOOM_API_SECRET* - available [from Zoom](https://support.zoom.us/hc/en-us/community/posts/115010739366-How-to-find-API-Key-API-Secret-)
    - *ZOOM_UID* - the e-mail ID of the Zoom account that will host the meeting
- Use RigD's "create rigd custom activity" command to define your meeting-starting activity
- Use one of the sample utterances your provided in the activity definition to start a Zoom meeting
