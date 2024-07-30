import requests

VERSION = "v16.0"
PHONE_NUMBER_ID = "117947841271318"
ENDPOINT = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
WHATSAPP_API_KEY = "EAADWMgrenekBAB23vZBVT3VfgPeK2OWaPG9PcSQB5RrZAQZAXZAZCJQmdaeuAZCY03kCbxdP6O6T4s0qVKicAyN8Ef6CQAexjbZAeSLOieIQ1Wh8vLaxstlU5iwZCDmRWcaosw6ZCZBzhQNLdmNWSpxTxJ6OtRqTWORzg9yubXNv8OX8dDZAzlEBxAyCZCaKV8Fn5bhVKi4JuhgKCEvzj7kO1XkPoW9B3lZAWvKsZD"

def send_message():
    template_name = "welcome_eprom"
    recipient = "351918402013"
    language_code = "en"
    institution_name = "Hospital"
    patient_name = "Promptly Test"
    disease_name = "Diabetes"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            },
            "components": [
                {
                    "type" : "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": institution_name
                        }
                    ]
                },
                {
                    "type" : "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": patient_name
                        },
                        {
                            "type": "text",
                            "text": disease_name
                        },
                        {
                            "type": "text",
                            "text": institution_name
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type" : "url",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "login"
                        }
                    ]
                },
            ]
        }
    }

    response = requests.post(
        url=ENDPOINT,
        json=payload,
        headers=headers,
        timeout=300,
    )

    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    send_message()