import os
import requests
import json
import questions_mock
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='example.env')
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
WEBHOOKVERIFYTOKEN = os.getenv("VERIFY_TOKEN") 

# Configure logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("responses.log"),  # Output file for logs
        logging.StreamHandler()  # Output logs to console as well
    ]
)

def send_whatsapp_template_message(phone_number):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {"name": "questionary", "language": {"code": "en"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response

def send_message(recipient, text):
    data = get_text_message_input(recipient, text)
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    # response = requests.post(url, data=data, headers=headers)
    #if response.status_code == 200:
    #    print("Body:", response.text)
    #else:
    #    print(response.text)

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

# Dictionary to track the current state of each user, using the phone number as the key.
user_states = {}

questions = questions_mock.questions

def handle_questionnaire(message):
    phone_number = message.get('from')
    text = None


    # Extract text or button reply from the message
    if 'text' in message:
        text = message['text'].get('body')
    if 'button' in message:
        text = message['button'].get('payload') 
    else:
        logging.warning("No recognizable message content found")

    # Initialize user state if not existing
    if phone_number not in user_states:
        user_states[phone_number] = -1  # Start at -1 to check the template response

    # Check if the response to the template is "yes" to start the questionnaire
    if user_states[phone_number] == -1:
        if text == "yes":  # Check if the response is "yes"
            user_states[phone_number] = 0
            first_question = questions[0]['question']
            send_message(phone_number, first_question)
        else:
            # If the response is not "yes", keep the state at -1 and do not start the questionnaire
            return

    # If the user is already in the questionnaire and has responded, process the response
    elif text is not None:
        current_question_index = user_states[phone_number]

        # Log the user's response and send the next question, if available
        if current_question_index >= 0 and current_question_index < len(questions):
            question = questions[current_question_index]['question']
            logging.info(f"Question: {question}, Answer: {text}")
            user_states[phone_number] += 1

        if user_states[phone_number] < len(questions):
            next_question = questions[user_states[phone_number]]['question']
            send_message(phone_number, next_question)
        else:
            logging.info("All questions have been asked.")
            user_states.pop(phone_number)
            
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WEBHOOKVERIFYTOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        return "Forbidden", 403    


def process_message(message):
    handle_questionnaire(message)

def start_questionnaire(phone_number):
    if phone_number not in user_states:
        user_states[phone_number] = -1
    send_whatsapp_template_message(phone_number)
