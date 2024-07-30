from flask import Flask, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv(dotenv_path='example.env')
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

WEBHOOKVERIFYTOKEN = "1234"  # Set your webhook verify token here

questions = [
    {"question": "What is your name?", "category": "personal"},
    {"question": "How are you feeling today?", "category": "health"},
    {"question": "What is your favorite color?", "category": "personal"},
]

# Send Template
def send_whatsapp_template_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": "351910134981",
        "type": "template",
        "template": {"name": "questionary", "language": {"code": "en"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# Send Message
def send_message(recipient, text):
    data = get_text_message_input(recipient, text)
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
    else:
        print(response.status_code)
        print(response.text)

# Format the text message in JSON to send via API
def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

#Dictionary to track the current state of each user, using the phone number as the key.
user_states = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data and 'entry' in data:
        for entry in data['entry']:
            if 'changes' in entry:
                for change in entry['changes']:
                    if 'value' in change and 'messages' in change['value']:
                        for message in change['value']['messages']:
                            phone_number = message['from']
                            text = None

                            if 'text' in message:
                                text = message['text']['body']
                            elif 'interactive' in message and 'button_reply' in message['interactive']:
                                text = message['interactive']['button_reply']['title']

                            if phone_number not in user_states:
                                user_states[phone_number] = -1  # Initialize at -1 to send the first question

                            if user_states[phone_number] == -1:
                                user_states[phone_number] = 0
                                first_question = questions[0]['question']
                                send_message(phone_number, first_question)
                                continue

                            # Check if the text is not None
                            if text is not None:
                                # Process the current message
                                current_question_index = user_states[phone_number]

                                if current_question_index >= 0 and current_question_index < len(questions):
                                    print(f"User's response to '{questions[current_question_index]['question']}': {text}")
                                    user_states[phone_number] += 1

                                # Send the next question
                                if user_states[phone_number] < len(questions):
                                    next_question = questions[user_states[phone_number]]['question']
                                    send_message(phone_number, next_question)
                                else:
                                    print("All questions have been asked.")
                                    # Optionally reset the state or handle the end of the questionnaire
                                    user_states.pop(phone_number)
                                    continue

    return "EVENT_RECEIVED", 200

@app.route('/webhook', methods=['GET'])
def webhookverification():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WEBHOOKVERIFYTOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        return "Forbidden", 403

if __name__ == "__main__":
    # Send the template message manually before starting the server
    response = send_whatsapp_template_message()
    if response.status_code == 200:
        print("Template sent successfully.")
    else:
        print("Failed to send template.")
        print(response.status_code)
        print(response.text)

    app.run(port=8000, debug=True)
