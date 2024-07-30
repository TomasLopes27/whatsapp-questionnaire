import requests
import json
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path='example.env')

# Obter as variáveis de ambiente
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")




# questions
#questions = {
#    1: {"question": "What is your name?", "category": "personal"},
#    2: {"question": "How are you feeling today?", "category": "health"},
#    3: {"question": "What is your favorite color?", "category": "personal"},
#}


# --------------------------------------------------------------
# Send a custom text WhatsApp message
# --------------------------------------------------------------

# NOTE: First reply to the message from the user in WhatsApp!


def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": 351910134981,
        "type": "template",
        "template": {"name": "questionary ", "language": {"code": "en"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# Call the function
response = send_whatsapp_message()
print(response.status_code)
print(response.json())





