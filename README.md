# WhatsApp Questionnaire
WhatsApp Questionnaires API

This project sets up a Flask server to send questionnaires and receive responses via the WhatsApp API.

## Installing and Running the Project

### Requirements

- `pip install -r requirements.txt`

### Installation

1. Start the Flask server:
```bash
python run.py
```
2. Command to create an SSH tunnel and expose the local server:
```bash
$ ssh -R 80:localhost:8000 serveo.net
```

3.Webhook Verification::
```bash
$ https://<your-subdomain>.serveo.net/webhook
```
3.1 Verification Code: 1234
