import os, requests, json, logging, questions_mock, settings
from flask import request
import pdb;

# Configure logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("responses.log"),  # Output file for logs
        logging.StreamHandler()  # Output logs to console as well
    ]
)

def send_whatsapp_template_message(phone_number, name):
    url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + settings.ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {"name": name, "language": {"code": "en"}},
    }
    response = requests.post(url, headers=headers, json=data)
    
    return response

def send_message(recipient, text):
    data = get_text_message_input(recipient, text)
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer " + settings.ACCESS_TOKEN,
    }
    url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/messages"

    requests.post(url, data=data, headers=headers)

    """
    if response.status_code == 200:
        print("Body:", response.text)
    else:
        print(response.text)
    """    

def send_interactive_message(phone_number, question, buttons):
    url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": "Bearer " + settings.ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": question
            },
            "action": {
                "buttons": [
                    {"type": "reply", "reply": button} for button in buttons
                ]
            }
        }
    }   

    requests.post(url, headers=headers, json=data)

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

questions = questions_mock.questions

def write_response_to_file(phone_number, question_index, question, answer):
    filename = f"responses_{phone_number}.log"
    with open(filename, 'a') as file:
        file.write(f"Question {question_index + 1}: {question}\nAnswer: {answer}\n")

def print_status(status):
    return logging.info(status)        

def read_last_question_from_file(phone_number):
    filename = f"responses_{phone_number}.log"
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if line.startswith("Question "):
                question_index = int(line.split(" ")[1].strip(":")) - 1
                return question_index
    return None

def get_next_question_index(last_question_index):
    if last_question_index is None:
        return 0  # No questions have been asked yet
    return last_question_index + 1

def handle_questionnaire(phone_number,text):
    last_question_index = read_last_question_from_file(phone_number)

    # If starting questionnaire, verify if the user says "yes" or "no"
    if last_question_index is None:
        if text.lower() == "yes":
            send_question(phone_number,0)
            return
        elif text.lower() == "no":
            return

    # Handles the case where the server restarts and continues the questionnaire from the last saved point   
    if last_question_index is not None:
        if text.lower() == "yes":
            next_question_index = get_next_question_index(last_question_index)
            send_question(phone_number,next_question_index)
            return    
    
    next_question_index = get_next_question_index(last_question_index)

    # If already in questionnaire
    if next_question_index < len(questions):
        current_question = questions[next_question_index]['question']

        write_response_to_file(phone_number, next_question_index, current_question, text)

        if next_question_index + 1 < len(questions):
            send_question(phone_number,next_question_index + 1)
        else:
            logging.info("All questions have been asked.")
            send_message(phone_number, "Thank you for completing the questionnaire!")

#Send the question to the user
def send_question(phone_number, question_index):
    question = questions[question_index]['question']
    category = questions[question_index].get('category')

    if category == "interactive":
        buttons = questions[question_index].get('buttons', [])
        send_interactive_message(phone_number, question, buttons)
    elif category == "text":
        send_message(phone_number, question)            
        
def isVerify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == settings.WEBHOOKVERIFYTOKEN:
        logging.info("Webhook verified successfully!")
        return True, challenge
    else:
        return False, None

def process_message(message):
    handle_questionnaire(message)

def start_questionnaire(phone_number):
    send_whatsapp_template_message(phone_number,"questionary")