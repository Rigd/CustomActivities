##### Purpose
This is an AWS lambda module that allows custom activities to send text messages through Twilio.
##### Deployment
- Clone the repository
- Zip this directory (twilio)
- Use RigD's "create lambda function" activity to deploy the lambda to AWS 
    - use "Python 3.6" runtime
    - make sure Python module "twilio" is available to the lambda
- Set the following environment variables in the newly created lambda:
    - *TWILIO_ACCOUNT_SID* - available from the [General Settings](https://www.twilio.com/console/project/settings) section of your Twilio Dashboard. 
    - *TWILIO_AUTH_TOKEN* - available from the [General Settings](https://www.twilio.com/console/project/settings) section of your Twilio Dashboard. 
    - *TWILIO_PHONE_NUMBER* - One of your SMS-enabled [Twilio numbers](https://www.twilio.com/console/phone-numbers/incoming)
- Use RigD's "create rigd custom activity" command to define your text-sending activity (slots "To" and "Body" are required)
- Use one of the sample utterances you provided in the activity definition to send a text message
