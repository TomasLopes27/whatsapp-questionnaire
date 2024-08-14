# WhatsApp Questionnaire
WhatsApp Questionnaires API

This project sets up a Flask server to send questionnaires and receive responses via the WhatsApp API.

## Installing and Running the Project

### Requirements

`pip install -r requirements.txt`

### Installation

1. Start the Flask server:

```bash
python app.py
```

#### Launch ngrok

The steps below are taken from the [ngrok documentation](https://ngrok.com/docs/integrations/whatsapp/webhooks/).

> You need a static ngrok domain because Meta validates your ngrok domain and certificate!

Once your app is running successfully on localhost, let's get it on the internet securely using ngrok!

1. If you're not an ngrok user yet, just sign up for ngrok for free.
2. Download the ngrok agent.
3. Go to the ngrok dashboard, click Your [Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken), and copy your Authtoken.
4. Follow the instructions to authenticate your ngrok agent. You only have to do this once.
5. On the left menu, expand Cloud Edge and then click Domains.
6. On the Domains page, click + Create Domain or + New Domain. (here everyone can start with [one free domain](https://ngrok.com/blog-post/free-static-domains-ngrok-users))
7. Start ngrok by running the following command in a terminal on your local desktop:

```
ngrok http 8000 --domain your-domain.ngrok-free.app
```

8. ngrok will display a URL where your localhost application is exposed to the internet (copy this URL for use with Meta).


#### Integrate WhatsApp

In the Meta App Dashboard, go to WhatsApp > Configuration, then click the Edit button.
1. In the Edit webhook's callback URL popup, enter the URL provided by the ngrok agent to expose your application to the internet in the Callback URL field, with /webhook at the end (i.e. https://myexample.ngrok-free.app/webhook).
2. Enter a verification token. This string is set up by you when you create your webhook endpoint. You can pick any string you like. Make sure to update this in your `VERIFY_TOKEN` environment variable.
3. After you add a webhook to WhatsApp, WhatsApp will submit a validation post request to your application through ngrok. Confirm your localhost app receives the validation get request and logs `WEBHOOK_VERIFIED` in the terminal.
4. Back to the Configuration page, click Manage.
5. On the Webhook fields popup, click Subscribe to the **messages** field. Tip: You can subscribe to multiple fields.


### Starting the Questionnaire

To start the questionnaire, send a GET request to the following endpoint, replacing <phone_number> with the recipient's phone number:

```
http://localhost:8000/start_questionnaire?phone_number=<phone_number>
```
This will send the initial template message to the specified phone number, prompting the user to start the questionnaire.

### Collecting Responses

Responses will be processed and saved in individual log files named responses_<phone_number>.log. Each file contains the questions and corresponding answers from the user. The format of each log entry is as follows:

```
Question <number>: <question_text>
Answer: <user_response>
```
### Viewing Responses
You can view a user's responses by opening their corresponding log file in the project directory. The log file is named using the user's phone number, e.g., responses_<phone_number>.log.

These logs allow you to easily reference and analyze the responses provided by each user.





